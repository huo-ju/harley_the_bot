import sys
import re
import db_data as datadb

def clean_text(text):
    text = re.sub(r'(\r|\n)', '', text, flags=re.MULTILINE)
    text = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z0-9\&\.\/\?\:@\-_=#])*', '', text, flags=re.MULTILINE)
    return text

def clean_englishandchar(text):
    text = re.sub(r'[a-zA-Z0-9$@$!%*?&#^-_.\', +/:]+', '', text, flags=re.MULTILINE)
    return text



def formatline(format, data):
    line = ""
    if format=="train":
        line = str(data[1])+"\t"+str(data[0])+"\ta\t"+ clean_text(data[2])
    elif format=="test":
        line = str(data[1])+"\t" + clean_text(data[2])

    return line

def export_train(number):
    tweets = datadb.load_data_by_tag(0, int(number/3))
    for tweet in tweets:
        line = formatline("train", tweet)
        print(line)

    tweets = datadb.load_data_by_tag(1, int(number/3*2))
    for tweet in tweets:
        line = formatline("train", tweet)
        print(line)


def export_train_notag(start, number):
    tweets = datadb.load_data_no_tag(start,number)
    for tweet in tweets:
        line = formatline("train", tweet)
        print(line)

def export_test_notag(start, number):
    print("id\tsentence")
    tweets = datadb.load_data_no_tag(start,number)
    for tweet in tweets:
        line = formatline("test", tweet)
        print(line)

def export_test(number):
    print("id\tsentence")
    tweets = datadb.load_data_by_tag(0, number)
    for tweet in tweets:
        line = formatline("test", tweet)
        print(line)
    tweets = datadb.load_data_by_tag(1, number)
    for tweet in tweets:
        line = formatline("test", tweet)
        print(line)

def cleandb():
    start = 0
    count = 50
    while True:
        tweets = datadb.load_data_for_clean(start, count);
        print ("info: " + str(start)+" "+ str( count )+ " "+ str(len(tweets)))
        if len(tweets)==0:
            print("clean task done.")
            break
        for tweet in tweets:
            outputtext = clean_englishandchar(tweet[3])
            if len(outputtext) < 6:
                datadb.delete_data(tweet[0])
        datadb.commit()
        start = start + count

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("./export.py test [num] | train [num] |cleandb \n")
    elif sys.argv[1]=="cleandb":
        cleandb()
    elif sys.argv[1]=="test":
        num = 2000
        if len(sys.argv) == 3:
            num = int(sys.argv[2])
        export_test(num)
    elif sys.argv[1]=="train":
        num = 20
        if len(sys.argv) == 3:
            num = int(sys.argv[2])
        export_train(num)
    elif sys.argv[1]=="test_notag":
        start = 0
        num = 20
        if len(sys.argv) == 3:
            num = int(sys.argv[2])
        if len(sys.argv) == 4:
            start = int(sys.argv[2])
            num = int(sys.argv[3])
        export_test_notag(start, num)
    elif sys.argv[1]=="train_notag":
        start = 0
        num = 20
        if len(sys.argv) == 3:
            num = int(sys.argv[2])
        if len(sys.argv) == 4:
            start = int(sys.argv[2])
            num = int(sys.argv[3])
        export_train_notag(start, num)
