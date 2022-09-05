import json


class ReadJSON(object):
    keys = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E",
            5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A",
            10: "B Flat"}

    def __init__(self):
        pass

    def replace_single_quotes(self, file):
        with open(file, 'r') as f:
            filedata = f.read()
        # Replace the target string
        filedata = filedata.replace('\'', '\"')

        # Write the file out again
        with open(file, 'w') as f:
            f.write(filedata)
            # print(str(filedata))
            data = str(filedata)

    def parse_json(self, file):
        with open(file, 'r') as f:
            filedata = f.read()
            json_contents = json.loads(filedata)

        # for i in jsonT:
        # print(i)
        print("\nSONG FEATURES")
        print("\n-----------------------------------")
        print("\nBPM: ", json_contents[0]['tempo'])

        print("\nKey: ", self.keys.get(json_contents[0]['key']))

        print("\nTime Signature", json_contents[0]['time_signature'])

        print("\nLoudness: ", json_contents[0]['loudness'])

        print("\nAcousticness: ", json_contents[0]['acousticness'])

        print("\nDanceability", json_contents[0]['danceability'])

        dict_return = {"BPM": json_contents[0]['tempo'], "key": json_contents[0]['key'],
                       "time sig": json_contents[0]['time_signature'], "loudness": json_contents[0]['loudness'],
                       "acousticness": json_contents[0]['acousticness'],
                       "danceability": json_contents[0]['danceability']}

        return dict_return


if __name__ == "__main__":
    r_json = ReadJSON()
    r_json.replace_single_quotes("FeatSong0.json")
    r_json.parse_json("FeatSong0.json")
