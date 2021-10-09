import os
import shutil
from time import sleep
from tkinter import *
import sys
import PIL
import magic
from PIL import Image
from nudenet import NudeDetector

# Define
min_face_size = 0
min_breast_size = 0
min_ass_size = 0
min_pussy_size = 0
min_closeup_size_face = 30
min_closeup_size_breasts = 30
min_closeup_size_pussy = 30
min_closeup_size_ass = 30
min_closeup_size_feet = 10

cwd = sys.argv[-1]
detector = NudeDetector()
workdir = sys.argv[1]
todir = sys.argv[-1]

# Switches
move = False  # True = move orginal False = copy orginal
delete = False
type = 'gif'  # gif / image
debugshow = False
if not debugshow:
    print('nodebug')
    sleep(1)
# r=root, d=directories, f = files
for r, d, f in os.walk(workdir, topdown=True):
    for file in f:
        # Orginal file and maps
        imgfileorg = os.path.join(r, file).lower()
        basenameorg = os.path.join(str(os.path.basename(os.path.dirname(imgfileorg))))
        drive_tailorg = os.path.join(str(os.path.splitdrive(imgfileorg[1])))
        imgorg = os.path.join(str(os.path.basename(imgfileorg)))
        copyorg = os.path.join(todir, basenameorg, drive_tailorg[1], imgorg)
        mkdirorg = os.path.join(todir, basenameorg, drive_tailorg[1])
        # Print variable
        if debugshow:
            print('############################################################')
            print('Imagefileorg:\t' ,imgfileorg)
            print('Basenameorg:\t', basenameorg)
            print('Drive tail:\t', drive_tailorg)
            print('Imgorg:\t\t', imgorg)
            print('copyorg:\t', copyorg)
            print('mkdirorg:\t\t', mkdirorg)
            print('############################################################')
            sleep(1)
        # End print
        # New File and maps
        imgfilenew = os.path.join(r, file).lower()
        basenamenew = os.path.join(str(os.path.basename(os.path.dirname(imgfilenew))))
        drive_tailnew = os.path.join(str(os.path.splitdrive(imgfilenew[1])))
        imgnew = os.path.join(str(os.path.basename(imgfilenew)))
        copynew = os.path.join(todir, basenamenew, drive_tailnew[1], imgnew)
        mkdirnew = os.path.join(todir, basenamenew, drive_tailnew[1])
        # Print variable
        if debugshow:
            print('############################################################')
            print('Imagefilenew:\t', imgfilenew)
            print('Basenamenew:\t', basenamenew)
            print('Drive tailnew:\t', drive_tailnew)
            print('Imgnew:\t\t', imgnew)
            print('copynew:\t', copynew)
            print('mkdirnew:\t\t', mkdirnew)
            print('############################################################')
            sleep(1)
        # End print
        # Mime
        try:
            mime = magic.from_file(imgfileorg, mime=True)
        except:
            continue
        mime = mime.split('/')
        imgfileext = imgfileorg.split('.', 1)
        imgfileext = imgfileext[0]
        imgfilenew = imgfileext+'.'+mime[-1]
        imgnew = os.path.join(str(os.path.basename(imgfilenew)))
        filecopynew = os.path.join(cwd, 'Maps', 'Orgineel', basenamenew, imgnew)
        if os.path.exists(filecopynew):
            print('EXIST: ' ,filecopynew)
            continue

        basenamenew = os.path.join(str(os.path.basename(os.path.dirname(imgfilenew))))
        imgnew = os.path.join(os.path.basename(imgfilenew))
        print(mime[-1])
        #sleep(0.3)
        if not type in mime:
            print('\r\t\t\t\t\t\t\t\t', end='')
            print('\rNo, Image File' + ' ' + str(mime),basenameorg, end='')
            continue
        # Mime \\END
        # Print mime
        if debugshow:
            print('############################################################')
            print('Newname:\t', imgnew)
            print('############################################################')
            sleep(1)
        try:
            image = PIL.Image.open(imgfileorg)
        except:
            print('\r\t\t\t\t\t\t\t\t', end='')
            print('\rImagefile error')
            sleep(1)
            if delete == True:
                os.remove(imgfileorg)
            continue
        width, height = image.size
        size = (width * height) / 100
        orgsize = (width * height)
        if debugshow:
            print('############################################################')
            print ("Image Size: "+str(width)+" * "+str(height)+" = "+str(size))
            print('############################################################')
        image.close()
        # Detector
        noexposed = 0
        try:
            print('\r\t\t\t\t\t\t\t\t', end='')
            print('\rDetector: Fast', end='')
            detected = detector.detect(imgfileorg, mode='fast')
            olddetected = detected
            if debugshow:
                for d in detected:
                    print(d['label'])
                sleep(1)
        except OSError as error:
            print('############################################################')
            print('\rOS ERROR')
            sleep(1)
            try:
                print('############################################################')
                print('\rremove File: ',imgfileorg)
                if delete is True:
                    os.remove(imgfileorg)
                sleep(1)
            except:
                print('############################################################')
                print('\rProblem with remove: ',imgfileorg)
                sleep(5)
                continue
            continue
        skip = 0
        if len(detected) > 0:
            for d in detected:
                if 'EXPOSED' in d['label']:
                    skip += 1
            if skip == 0:
                noexposed = 1
                print('\r\t\t\t\t\t\t\t\t', end='')
                print('\rDetector: Slow', end='')
                print(orgsize)
                if orgsize > (640 * 480):
                    detected = detector.detect(imgfileorg)
                if debugshow:
                    for d in detected:
                        print(d['label'])
                    sleep(1)
            skip1 = skip
            for d in detected:
                if 'EXPOSED' in d['label']:
                    skip += 1
            if len(detected) == 0 or skip > skip1:
                print('\r\t\t\t\t\t\t\t\t', end='')
                print('\rDetector: Fast > Slow, no succes', end='')
                #sleep(0.3)
                detected = olddetected #detector.detect(imgfileorg, mode='fast')
                if debugshow:
                    for d in detected:
                        print(d['label'])
                    sleep(1)
        if debugshow:
            print('Go to Labels')
        # Finisch Detector
        ###############################################################################
        #######Labeling################################################################
        ###############################################################################
        x = ''
        butt = 0
        ebutt = 0
        epussy = 0
        ebreast = 0
        belly = 0
        face = 0
        woman = 0
        dick = 0
        male = 0
        covered = 0
        breast = 0
        pussy = 0
        exposed = 0
        detected_tags = set()
        breast_size = 0
        face_size = 0
        ass_size = 0
        feet_size = 0
        pussy_size = 0

        for d in detected:
            if d['label'] == 'FACE_F':
                if d['score'] > 0.7:
                    face_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
                    if (face_size / size) > min_face_size:
                        #detected_tags.add("FACE")
                        woman += 1
                        face += 1
                    if (face_size / size) > min_closeup_size_face:
                        detected_tags.add("FCLOSE")
            if d['label'] == 'COVERED_BREAST_F' and d['score'] > 0.8:
                breast_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
                if (breast_size / size) > min_breast_size:
                    detected_tags.add("CBREAST")
                    covered += 1
                    breast += 1
            if d['label'] == 'EXPOSED_BREAST_F':
                breast_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
                if (breast_size / size) > min_breast_size:
                    detected_tags.add("EBREAST")
                    exposed += 1
                    breast += 1
                    ebreast += 1
                if (breast_size / size) > min_closeup_size_breasts:
                    if d['score'] > 0.8:
                        detected_tags.add("BCLOSE")
            if d['label'] == 'COVERED_GENITALIA_F' and d['score'] > 0.8:
                pussy_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
                if (pussy_size / size) > min_pussy_size:
                    detected_tags.add("CPUSSY")
                    covered += 1
                    pussy += 1
            if d['label'] == 'EXPOSED_GENITALIA_F':
                pussy_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
                if (pussy_size / size) > min_pussy_size:
                    detected_tags.add("EPUSSY")
                    exposed += 1
                    pussy += 1
                    epussy += 1
                if (pussy_size / size) > min_closeup_size_pussy:
                    if d['score'] > 0.8:
                        detected_tags.add("PCLOSE")

            # if d['label'] == 'COVERED_BUTTOCKS':
            #     ass_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
            #     if (ass_size / size) > min_ass_size:
            #         #detected_tags.add("CASS")
            #         covered += 1
            #         butt += 1
            # if d['label'] == 'EXPOSED_BUTTOCKS':
            #     ass_size += (d['box'][2] - d['box'][0]) * (d['box'][3] - d['box'][1])
            #     if (ass_size / size) > min_ass_size:
            #         #detected_tags.add("EASS")
            #         exposed += 1
            #         butt += 1
            #         ebutt += 1
            #     if (ass_size / size) > min_closeup_size_ass:
            #         detected_tags.add("ACLOSE")
            # if d['label'] == 'EXPOSED_ANUS':
            #     detected_tags.add("EASS")
            #     exposed += 1
            #     ebutt += 1
            #     butt += 1
            # if d['label'] == 'EXPOSED_GENITALIA_M':
            #     dick += 1
            # if d['label'] == 'FACE_M':
            #     male += 1
            if d['label'] == 'EXPOSSED_BELLY':
                belly += 1
            # if d['label'] == 'EXPOSED_BREAST_M':
            #     male += 1
            # if '_M' in d['label']:
            #     male += 1


        if woman > 0 and ebreast > 1 and epussy > 0:
            detected_tags.add("NAKED")
        # if woman > 1 and ebreast > 1 and epussy > 1:
        #     detected_tags.add("NAKED" + str(woman))
        if epussy > 1:
            if exposed > 0:
                detected_tags.add("EPUSSIES")
        if ebreast > 2:
            if exposed > 0:
                detected_tags.add("EBOOBS")

        if woman > 1 and ebreast > 0 and epussy > 0:
            detected_tags.add('GIRLS')
        if epussy > 0:
            if covered == 0:
                if ebreast == 0:
                    if ebutt == 0:
                        detected_tags.add('ONLYPUSSY')
        if ebreast > 0:
            if covered == 0:
                if epussy == 0:
                    detected_tags.add('ONLYBREAST')
        if ebutt > 0:
            if covered == 0:
                if ebreast == 0:
                    if epussy == 0:
                        detected_tags.add('ONLYBUTT')
        #############################################################################
        #############MALE############################################################
        #############################################################################
        if male > 0:
            detected_tags.clear()
            detected_tags.add('MALE')
            if dick > 0:
                detected_tags.add('DICK')
        if dick > 0:
            detected_tags.clear()
            detected_tags.add('DICK')
        ########################################################################################
        #FileCopy
        ########################################################################################
        if len(detected_tags) > 0:

            if debugshow:
                print('##############################################')
                print('Filecopy part')
                print('##############################################')
                sleep(1)

            tag = ''
            for x in detected_tags:
                tag = (' '.join(list(detected_tags)))
                filecopynew = os.path.join(cwd, 'Maps', 'Orgineel', basenamenew, imgnew)
                mapcopynew = os.path.join(cwd, 'Maps', 'Orgineel', basenamenew)
                mkdir = os.path.join(cwd, 'Maps', 'Labels', x, basenamenew)
                mklink = os.path.join(cwd, 'Maps', 'Labels', x, basenamenew, imgnew)
                if debugshow:
                    print('##############################################')
                    print('mapcopynew :',mapcopynew)
                    print('mkdir :',mkdir)
                    print('##############################################')
                    sleep(1)
                if not os.path.exists(mapcopynew):
                    os.makedirs(mapcopynew)
                if not os.path.exists(mkdir):
                    os.makedirs(mkdir)
                # print('',tag)
                # print('Orgineel',filecopyorg)
                if move is False:
                    print('Move: ', imgfileorg, '>', filecopynew)
                    if not os.path.exists(filecopynew):
                        #print('copy:')
                        shutil.copy(imgfileorg, filecopynew)
                else:
                    if not os.path.exists(filecopynew):
                        #print('move:')
                        shutil.move(imgfileorg, filecopynew)

                if not os.path.exists(mklink):
                    shutil.copy(filecopynew, mklink)
                if x == '':
                    detected_tags = set()
            print('\r\t\t\t\t\t\t\t\t', end='')
            print('\r ', basenamenew, '', tag,': ',imgnew)
        else:
            print('\rNot Tags > Remove:', imgfileorg, end='')
            if delete is True:
                os.remove(imgfileorg)

        # exit()

        # print closeup values, for debugging
        # print ("face="+str(face_size/size)+" boobs="+str(breast_size/size)+" ass="+str(ass_size/size)+" pussy="+str(pussy_size/size))
        continue






