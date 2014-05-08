========================
Pipic
========================

1 - What is it?
2 - Dependancies
3 - How to install

========================

1 -What is it?

Pipic was developed mainly for 3 resons:
    - Learn Python
    - Play with Raspberry Pi, Arduino and some eletronic stuff
    - Take pictures of my cat while I'm traveling (='.'=)

It performs the following flow:
    - Checks every {n} seconds an Gmail account
    - Verify if there is non-read email
    - If there is new email, then check if is a allowed email
    - Takes a picture and send to the allowed email sender or a custom "Pictures Not Allowed" pic to not allowed emails
    - Mark the email as read

Pipic is adapted to work with motion (https://github.com/sackmotion/motion) in case they need to run together. 
(e.g. Run motion for live stream while taking pictures with Pipic)

========================

2 - Dependencies

    Linux
        - fswebcam (https://github.com/fsphil/fswebcam) - Tested in Raspian (Raspberry PI Model B), LUMBUTU (eee-pci) 
    Mac OS X
        - ImageSnap (http://iharder.sourceforge.net/current/macosx/imagesnap/)

========================

3 - How to install

    git clone https://github.com/andersenmp/pipic.git
    
    Copy pipic/src/parameters.dpl to pipic/src/parameters.ini
    
    Configure pipic/src/parameters.ini

    [app]
    version = 0.0
    standby_time = 15
    allowed_emails = email@gmail.com

    [gmail]
    user = email@gmail.com
    password = pass4Email

    [motion]
    present = 0
