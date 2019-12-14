import tensorflow as tf
import tokenization
import json
import os
import collections

#os.environ["CUDA_VISIBLE_DEVICES"]="2"

class DataProcessor(object):
  """Base class for data converters for sequence classification data sets."""

  def get_train_examples(self, data_dir):
    """Gets a collection of `InputExample`s for the train set."""
    raise NotImplementedError()

  def get_dev_examples(self, data_dir):
    """Gets a collection of `InputExample`s for the dev set."""
    raise NotImplementedError()

  def get_test_examples(self, data_dir):
    """Gets a collection of `InputExample`s for prediction."""
    raise NotImplementedError()

  def get_labels(self):
    """Gets the list of labels for this data set."""
    raise NotImplementedError()

  @classmethod
  def _read_tsv(cls, input_file, quotechar=None):
    """Reads a tab separated value file."""
    raise NotImplementedError()


class InputProcessor(DataProcessor):
  """Processor for the Input data set (GLUE version)."""

  def get_test_examples(self, data_list):
    """See base class."""
    return self._create_examples( data_list , "test")

  def get_labels(self):
    """See base class."""
    return ["0", "1"]

  def _create_examples(self, lines, set_type):
    """Creates examples for the training and dev sets."""
    examples = []
    for (i, line) in enumerate(lines):
      guid = "%s-%s" % (set_type, i)
      if set_type == "test":
        text_id = line[0]
        text_a = tokenization.convert_to_unicode(line[1])
      label = "0"
      examples.append(
          InputExample(guid=guid, text_a=text_a, text_b=None, label=label, text_id=text_id))
    return examples

class InputExample(object):
  """A single training/test example for simple sequence classification."""

  def __init__(self, guid, text_a, text_b=None, label=None, text_id=None):
    """Constructs a InputExample.

    Args:
      guid: Unique id for the example.
      text_a: string. The untokenized text of the first sequence. For single
        sequence tasks, only this sequence must be specified.
      text_b: (Optional) string. The untokenized text of the second sequence.
        Only must be specified for sequence pair tasks.
      label: (Optional) string. The label of the example. This should be
        specified for train and dev examples, but not for test examples.
    """
    self.guid = guid
    self.tid = text_id
    self.text_a = text_a
    self.text_b = text_b
    self.label = label

class InputFeatures(object):
  """A single set of features of data."""

  def __init__(self,
               input_ids,
               input_mask,
               segment_ids,
               label_id,
               is_real_example=True):
    self.input_ids = input_ids
    self.input_mask = input_mask
    self.segment_ids = segment_ids
    self.label_id = label_id
    self.is_real_example = is_real_example


class PaddingInputExample(object):
  """Fake example so the num input examples is a multiple of the batch size.

  When running eval/predict on the TPU, we need to pad the number of examples
  to be a multiple of the batch size, because the TPU requires a fixed batch
  size. The alternative is to drop the last batch, which is bad because it means
  the entire output data won't be generated.

  We use this class instead of `None` because treating `None` as padding
  battches could cause silent errors.
  """

def convert_single_example(ex_index, example, label_list, max_seq_length,
                           tokenizer):
  """Converts a single `InputExample` into a single `InputFeatures`."""

  if isinstance(example, PaddingInputExample):
    return InputFeatures(
        input_ids=[0] * max_seq_length,
        input_mask=[0] * max_seq_length,
        segment_ids=[0] * max_seq_length,
        label_id=0,
        is_real_example=False)

  label_map = {}
  for (i, label) in enumerate(label_list):
    label_map[label] = i

  tokens_a = tokenizer.tokenize(example.text_a)
  tokens_b = None
  if example.text_b:
    tokens_b = tokenizer.tokenize(example.text_b)

  if tokens_b:
    # Modifies `tokens_a` and `tokens_b` in place so that the total
    # length is less than the specified length.
    # Account for [CLS], [SEP], [SEP] with "- 3"
    _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
  else:
    # Account for [CLS] and [SEP] with "- 2"
    if len(tokens_a) > max_seq_length - 2:
      tokens_a = tokens_a[0:(max_seq_length - 2)]

  # The convention in BERT is:
  # (a) For sequence pairs:
  #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
  #  type_ids: 0     0  0    0    0     0       0 0     1  1  1  1   1 1
  # (b) For single sequences:
  #  tokens:   [CLS] the dog is hairy . [SEP]
  #  type_ids: 0     0   0   0  0     0 0
  #
  # Where "type_ids" are used to indicate whether this is the first
  # sequence or the second sequence. The embedding vectors for `type=0` and
  # `type=1` were learned during pre-training and are added to the wordpiece
  # embedding vector (and position vector). This is not *strictly* necessary
  # since the [SEP] token unambiguously separates the sequences, but it makes
  # it easier for the model to learn the concept of sequences.
  #
  # For classification tasks, the first vector (corresponding to [CLS]) is
  # used as the "sentence vector". Note that this only makes sense because
  # the entire model is fine-tuned.
  tokens = []
  segment_ids = []
  tokens.append("[CLS]")
  segment_ids.append(0)
  for token in tokens_a:
    tokens.append(token)
    segment_ids.append(0)
  tokens.append("[SEP]")
  segment_ids.append(0)

  if tokens_b:
    for token in tokens_b:
      tokens.append(token)
      segment_ids.append(1)
    tokens.append("[SEP]")
    segment_ids.append(1)

  input_ids = tokenizer.convert_tokens_to_ids(tokens)

  # The mask has 1 for real tokens and 0 for padding tokens. Only real
  # tokens are attended to.
  input_mask = [1] * len(input_ids)

  # Zero-pad up to the sequence length.
  while len(input_ids) < max_seq_length:
    input_ids.append(0)
    input_mask.append(0)
    segment_ids.append(0)

  assert len(input_ids) == max_seq_length
  assert len(input_mask) == max_seq_length
  assert len(segment_ids) == max_seq_length

  label_id = label_map[example.label]
  #if ex_index < 5:
  #  tf.logging.info("*** Example ***")
  #  tf.logging.info("guid: %s" % (example.guid))
  #  tf.logging.info("tokens: %s" % " ".join(
  #      [tokenization.printable_text(x) for x in tokens]))
  #  tf.logging.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
  #  tf.logging.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
  #  tf.logging.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
  #  tf.logging.info("label: %s (id = %d)" % (example.label, label_id))

  feature = InputFeatures(
      input_ids=input_ids,
      input_mask=input_mask,
      segment_ids=segment_ids,
      label_id=label_id,
      is_real_example=True)
  return feature



class Predict(object):

  def __init__(self, config):
    self.predict_fn = tf.contrib.predictor.from_saved_model(config["model_file"])
    self.processor = InputProcessor()
    self.label_list = self.processor.get_labels()
    self.max_seq_length = config["max_seq_length"];
    self.tokenizer = tokenization.FullTokenizer(vocab_file=config["vocab_file"], do_lower_case=config["do_lower_case"])

  def _get_examples_for_predict(self, input_data):
      predict_examples = self.processor.get_test_examples(input_data)
      examples = []
      def create_int_feature(values):
        f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
        return f
      for (ex_index, example) in enumerate(predict_examples):
          input_feature = convert_single_example(ex_index, example, self.label_list, self.max_seq_length, self.tokenizer)
          features = collections.OrderedDict()
          features["input_ids"] = create_int_feature(input_feature.input_ids)
          features["input_mask"] = create_int_feature(input_feature.input_mask)
          features["segment_ids"] = create_int_feature(input_feature.segment_ids)
          features["label_ids"] = create_int_feature([input_feature.label_id])
          features["is_real_example"] = create_int_feature(
              [int(input_feature.is_real_example)])
          
          tf_example = tf.train.Example(features=tf.train.Features(feature=features))
          examples.append(tf_example.SerializeToString())
      return examples
  def _post_processing(self, probabilities, input_data, screen_name):
    results = []
    c_1 = 0
    count = probabilities.shape[0]
    for i in range(0, count):
        itemresult = 0
        if (probabilities.item(i, 0) < probabilities.item(i, 1)):
            itemresult = 1
            c_1 += 1
        item ={} 
        item["data"] = {"id":input_data[i][0],"text":input_data[i][1]}
        item["probabilities"] = [probabilities.item(i, 0) , probabilities.item(i, 1)]
        item["classification"]=itemresult
        item["offset"]= "%.6f" % abs(probabilities.item(i, 0) - probabilities.item(i, 1))
        results.append(item)
    ratio = c_1/count
    summary = {"screen_name": screen_name, "ratio" : "%.6f" % ratio }
    return {"summary":summary, "results":results}
   
  def get_predictions(self, input_data, screen_name):
    examples_for_predict = self._get_examples_for_predict(input_data)
    predictions = self.predict_fn({'example': examples_for_predict})
    probabilities = predictions["probabilities"]
    results = self._post_processing(probabilities, input_data, screen_name)
    return results


