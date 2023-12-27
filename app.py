#!/usr/bin/python3

import base64
import os
import codecs
import httplib2
import xml.etree.ElementTree as et


nagra_solutions_url = ''
nv_authorizations = ''
streaming_mode = 'DASH'
xml = "text/xml"
headers = {
    'Content-Type': 'text/xml',
    'nv-authorizations': ""
}

def frame_xml(contentID):
    # xml data for request
    xml_data = """
    </soapenv:Envelope>
    """%(contentID)
    return xml_data



file_video_input = input('Enter video file name including file format such as .mp4: ')

while len(file_video_input) <= 0:
    file_video_input = input('Enter video file name including file format such as .mp4: ')

file_audio_input =  input('Enter audio file name including file format such as .mp4: ')

while len(file_audio_input) <= 0:
    file_audio_input =  input('Enter audio file name including file format such as .mp4: ')

encrypt_option = input('Would you like to content to be encrypted yes/no ?')

video_in_chunked = "'in={},stream=video,init_segment=chunked_content/video_init.mp4,segment_template=chunked_content/video$Number$.m4s' ".format(file_video_input)
audio_in_chunked = "'in={},stream=audio,init_segment=chunked_content/audio_init.mp4,segment_template=chunked_content/audio$Number$.m4s' ".format(file_audio_input)

os.system("sudo ~/bin/packager-linux {} {} --generate_static_mpd --segment_duration '30' --mpd_output chunked_content/h265.mpd ".format(video_in_chunked, audio_in_chunked))
os.system("sudo chmod 777 chunked_content")

if(encrypt_option.lower() == 'yes' or encrypt_option.lower() == 'y' ):
    content_id = input('Enter content key:')

    while len(content_id) <= 0:
        content_id = input('Enter content key:')


    xml_data = frame_xml(content_id)
    http = httplib2.Http('.cache')
    resp, content = http.request(nagra_solutions_url, 'POST', xml_data, headers)

    tree = et.fromstring(content.decode("utf-8"))
    elementtree = et.ElementTree(tree)
    root = elementtree.getroot()
    contentKey = root.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()
    psshBox = root.getchildren()[0].getchildren()[0].getchildren()[2].getchildren()[1].getchildren()[3]

    raw_keyid = contentKey[0].text
    keyid = raw_keyid.replace("-", "")
    key = contentKey[1].text
    iv = contentKey[2].text
    pssh_box = psshBox.text

    key_hex = codecs.encode(base64.b64decode(key), 'hex').decode("utf-8")
    iv_hex = codecs.encode(base64.b64decode(iv), 'hex').decode("utf-8")
    pssh_box_hex = codecs.encode(base64.b64decode(pssh_box), 'hex').decode("utf-8")

# For further assitance on shaka packager please look at the documentation -- https://github.com/google/shaka-packager

    video_in_encrypted = "'in={},stream=video,init_segment=encrypted_content/video_init.mp4,segment_template=encrypted_content/video$Number$.m4s' ".format(file_video_input)
    audio_in_encrypted = "'in={},stream=audio,init_segment=encrypted_content/audio_init.mp4,segment_template=encrypted_content/audio$Number$.m4s' ".format(file_audio_input)
    raw_encryption = "--enable_raw_key_encryption --keys key_id={}:key={} --iv={} --pssh {} --generate_static_mpd --segment_duration '30' --mpd_output encrypted_content/h265.mpd".format(keyid, key_hex, iv_hex, pssh_box_hex)

    os.system("sudo ~/bin/packager-linux {} {} {} ".format(video_in_encrypted, audio_in_encrypted, raw_encryption))
    os.system("sudo chmod 777 encrypted_content")


    print("Content Key ID: {} \n".format(keyid))
    print("Content Key: {} \n".format(key))
    print("Content Id Used: {} \n".format(content_id))
    text_file = open("encrypt_details.txt", "w")
    text_file.write("\n Contet Key Id: %s " % raw_keyid)
    text_file.write("\n Content ID: %s " % content_id)
    text_file.write("\n Contet Key: %s \n" % key)
    text_file.close()

    print("Please be sure to add Key and Key ID to the myCinema Portal: https://portal.mycinema.live")



os.system("sudo ~/bin/packager-linux {} {} --generate_static_mpd --segment_duration '30' --mpd_output chunked_content/h265.mpd ".format(video_in_chunked, audio_in_chunked))
os.system("sudo chmod 777 chunked_content")
