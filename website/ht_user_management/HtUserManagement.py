#!/usr/bin/env python
import csv
import pdb
import unittest
import os
import subprocess


class HtUserManagement():
    def __init__(self, db_filename):
        self.db_file = db_filename

    def __doesDbFileExist(self):
        return os.path.isfile(self.db_file)

    def __executeCmd(self, command, stderr=open(os.devnull)):
        ret = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=stderr)
        output = ret.communicate()[0]
        lines = output.split('\n')
        return lines

    def __createRandomPassword(self):
        """ Create a password of random length between 8 and 16
            characters long, made up of numbers and letters.
        """
        pwlen = randint(8,16)
        pw = self.__executeCmd("pwgen -1vBn " + str(pwlen))[0]

        return pw

    def __GetHtEncPassword(self, password):
        retVal = self.__executeCmd("htpasswd2 -bn user1 " + password)[0].split(':')[1]
        return retVal

    def __writeOutCsv(self, accountInfo):
        ofile = open(self.db_file, "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar='"')
        for row in accountInfo:
            writer.writerow(row)
        ofile.close()

    def writeOutHtpasswd(self, filename):
        if (os.path.isfile(filename)):
            raise Exception("Error: [" + filename + "] already exists!")

        accountInfo = self.__readInCsv()

        outFile = open(filename, "w")

        for curRow in accountInfo[1:]: #skip header line
            username = curRow[0]
            enc_password = curRow[2]
            outFile.write(username + ":" + enc_password + "\n")
        outFile.flush()
        outFile.close()

    def __verifyUsername(self, username):
        # this verifies that the username is an e-mail address
        if (' ' in username) or \
           (not '@' in username) or \
           (not '.' in username):
            raise Exception("Error: [" + username + "] is not a valid e-mail address.")

        if (username != username.lower()):
            raise Exception("Error: [" + username + "] is not all lower case.")

    def __readInCsv(self):
        if not self.__doesDbFileExist():
            return None

        ifile = open(self.db_file, "r")
        reader = csv.reader(ifile, delimiter=',', quotechar='"')
        accountInfo = []

        for curLine in reader:
            accountInfo.append(curLine)

        return accountInfo

    def listUsers(self):
        accountInfo = self.__readInCsv()

        for curLine in accountInfo[1:]: # skip over the header column
            print curLine[0]

    def doesUserExist(self, username):
        if not self.__doesDbFileExist():
            return False

        accountInfo = self.__readInCsv()

        for curAccount in accountInfo[1:]:
            if (curAccount[0].lower() == username.lower()):
                return True

        # we didn't find it above, so it's not in there
        return False

    def __sendEmail(self, to, subject, message):
        self.__executeCmd("echo \'" + message + "\' | mail -s \'" + subject + "\' -r mono@novell.com " + to)

    def emailOutNotifications(self, subject, invitation_filename):
        if not os.path.isfile(invitation_filename):
            raise Exception("Error: [" + invitation_filename + "] doesn't exist!")

        inFile = open(invitation_filename,"r")
        lines = inFile.readlines()
        msg = ''.join(lines)

        accountInfo = self.__readInCsv()
        for curAccount in accountInfo[1:]:
            username = curAccount[0]
            password = curAccount[1]
            fullName = curAccount[3]
            notified = curAccount[4]
            tmpMsg = msg.replace('{full_name}',fullName)
            tmpMsg = tmpMsg.replace('{username}',username)
            tmpMsg = tmpMsg.replace('{password}',password)

            if notified.lower() != "yes":
                print "emailing [" + username + "]"
                self.__sendEmail(username, subject, tmpMsg)
                self.setNotified(username)

    def addUser(self, username, password, full_name):
        self.addUserWithNotified(username, password, full_name, "")

    def addUserWithNotified(self, username, password, full_name, been_notified):
        enc_password = self.__GetHtEncPassword(password)

        if been_notified == "":
            been_notified = "no"

        been_notified = been_notified.lower()

        self.__verifyUsername(username)

        if self.doesUserExist(username):
            raise Exception("Error: [" + username + "] already exists!")

        if not self.__doesDbFileExist():
            self.__writeOutCsv([["username","password","enc_password","full_name","been_notified"]])

        accountInfo = self.__readInCsv()
        accountInfo.append([username, password, enc_password, full_name, been_notified])
        self.__writeOutCsv(accountInfo)

    def addUserWithRandomPassword(self, username, full_name):
        pw = self.__createRandomPassword()
        self.addUser(username, pw, full_name)

    def removeUser(self, username):
        self.__verifyUsername(username)

        if not self.doesUserExist(username):
            raise Exception("Error: [" + username + "] doesn't exist!")

        accountInfo = self.__readInCsv()
        newAccountInfo = []

        for curAccount in accountInfo:
            if (curAccount[0].lower() != username.lower()):
                newAccountInfo.append(curAccount)

        self.__writeOutCsv(newAccountInfo)

    def getUser(self, username):
        self.__verifyUsername(username)

        if not self.doesUserExist(username):
            raise Exception("Error: [" + username + "] doesn't exist!")

        accountInfo = self.__readInCsv()

        for curAccount in accountInfo:
            if (curAccount[0].lower() == username.lower()):
                return curAccount

    def updateUser(self, username, password, full_name, been_notified):
        self.__verifyUsername(username)

        if not self.doesUserExist(username):
            raise Exception("Error: [" + username + "] doesn't exist!")

        curUser = self.getUser(username)

        username = curUser[0] # make sure the update doesn't update the username

        enc_password = curUser[2]
        if password != curUser[1]: #they are setting a new password
            enc_password = self.__GetHtEncPassword(password)

        accountInfo = self.__readInCsv()
        newAccountInfo = []

        for curAccount in accountInfo:
            if (curAccount[0].lower() == username.lower()):
                newAccountInfo.append([username, password, enc_password, full_name, been_notified])
            else:
                newAccountInfo.append(curAccount)

        self.__writeOutCsv(newAccountInfo)

    def setNotified(self, username):
        userInfo = self.getUser(username)
        username = userInfo[0]
        password = userInfo[1]
        full_name = userInfo[3]
        notified = "yes"
        self.updateUser(username, password, full_name, notified)


class TestModule(unittest.TestCase):
    tstDb = "/tmp/tmp_user.db"
    user = HtUserManagement(tstDb)

    def setUp(self):
        if os.path.isfile(self.tstDb):
            os.remove(self.tstDb)

    def testSetNotified(self):
        self.user.addUser("rupert@novell.com", "mono", "Rupert Monkey")
        self.user.addUser("rupert_monkey@novell.com", "onom", "Rupert Monkey 2")

        # test to make sure it throws an exception if the user doesn't exist
        try:
            email = "nothing@crap.com"
            self.user.setNotified(email)
            self.assertEqual('Exception not raised!', email)
        except Exception,exc:
            self.assertEqual(str(exc), "Error: [" + email + "] doesn't exist!")

        self.user.setNotified("rupert@novell.com")

        # Check the file to make sure it's how it should be
        accountInfo = self.user._HtUserManagement__readInCsv()
        self.assertEqual(len(accountInfo), 3, "user_db is bigger than expected, expected 3, got " + str(len(accountInfo)))
        self.assertEqual(accountInfo[0], ["username","password","enc_password","full_name","been_notified"])
        self.assertEqual(accountInfo[1][0:2], ["rupert@novell.com", "mono"])
        self.assertEqual(accountInfo[1][3:],  ["Rupert Monkey","yes"])
        self.assertEqual(accountInfo[2][0:2], ["rupert_monkey@novell.com", "onom"])
        self.assertEqual(accountInfo[2][3:],  ["Rupert Monkey 2","no"])


    def testUpdateUser(self):
        self.user.addUser("rupert@novell.com", "mono", "Rupert Monkey")
        self.user.addUser("rupert_monkey@novell.com", "onom", "Rupert Monkey 2")

        # test to make sure it throws an exception if the user doesn't exist
        try:
            email = "nothing@crap.com"
            self.user.updateUser(email,"","","")
            self.assertEqual('Exception not raised!', email)
        except Exception,exc:
            self.assertEqual(str(exc), "Error: [" + email + "] doesn't exist!")

        self.user.updateUser("rupert@novell.com", "mono2", "Rupert Monkey2", "yes")

        # Check the file to make sure it's how it should be
        accountInfo = self.user._HtUserManagement__readInCsv()
        self.assertEqual(len(accountInfo), 3, "user_db is bigger than expected, expected 3, got " + str(len(accountInfo)))
        self.assertEqual(accountInfo[0], ["username","password","enc_password","full_name","been_notified"])
        self.assertEqual(accountInfo[1][0:2], ["rupert@novell.com", "mono2"])
        self.assertEqual(accountInfo[1][3:],  ["Rupert Monkey2","yes"])
        self.assertEqual(accountInfo[2][0:2], ["rupert_monkey@novell.com", "onom"])
        self.assertEqual(accountInfo[2][3:],  ["Rupert Monkey 2","no"])


    def testGetUser(self):
        self.user.addUser("rupert@novell.com", "mono", "Rupert Monkey")
        self.user.addUser("rupert_monkey@novell.com", "onom", "Rupert Monkey 2")

        # test to make sure it throws an exception if the user doesn't exist
        try:
            email = "nothing@crap.com"
            self.user.getUser(email)
            self.assertEqual('Exception not raised!', email)
        except Exception,exc:
            self.assertEqual(str(exc), "Error: [" + email + "] doesn't exist!")

        userInfo = self.user.getUser("rupert@novell.com")
        self.assertEqual(userInfo[0], "rupert@novell.com")
        self.assertEqual(userInfo[1], "mono")
        self.assertEqual(userInfo[3], "Rupert Monkey")


    def testRemoveUser(self):
        # Test without anything in the file
        try:
            email = "nothing@crap.com"
            self.user.removeUser(email)
            self.assertEqual('Exception not raised!', email)
        except Exception,exc:
            self.assertEqual(str(exc), "Error: [" + email + "] doesn't exist!")

        self.user.addUser("rupert@novell.com", "mono", "Rupert Monkey")
        self.user.addUser("rupert_monkey@novell.com", "onom", "Rupert Monkey 2")

        # Test with something in the file
        try:
            email = "nothing@crap.com"
            self.user.removeUser(email)
            self.assertEqual('Exception not raised!', email)
        except Exception,exc:
            self.assertEqual(str(exc), "Error: [" + email + "] doesn't exist!")

        self.user.removeUser("rupert@novell.com")
        accountInfo = self.user._HtUserManagement__readInCsv()
        self.assertEqual(len(accountInfo), 2, "user_db is bigger than expected, expected 2, got " + str(len(accountInfo)))
        self.assertEqual(accountInfo[0], ["username","password","enc_password","full_name","been_notified"])
        self.assertEqual(accountInfo[1][0:2], ["rupert_monkey@novell.com", "onom"])
        self.assertEqual(accountInfo[1][3:],  ["Rupert Monkey 2","no"])


    def testAddUserWithNotified(self):
        self.user.addUserWithNotified("rupert@novell.com", "mono", "Rupert Monkey","yes")
        # Check the file to make sure it's how it should be
        accountInfo = self.user._HtUserManagement__readInCsv()
        self.assertEqual(len(accountInfo), 2, "user_db is bigger than expected, expected 2, got " + str(len(accountInfo)))
        self.assertEqual(accountInfo[0], ["username","password","enc_password","full_name","been_notified"])
        self.assertEqual(accountInfo[1][0:2], ["rupert@novell.com", "mono"])
        self.assertEqual(accountInfo[1][3:],  ["Rupert Monkey","yes"])


    def testAddUser(self):
        users = [ ("rupert@novell.com", "mono", "Rupert Monkey", ""),
                  ("rupert_monkey@novell.com", "onom", "Rupert Monkey 2", ""),
                  ("rupert_monkey@novell.com", "onom", "Rupert Monkey 2", "Error: [rupert_monkey@novell.com] already exists!"),
                  ('Thomas@novell.com', "test", "Thomas Wiest", 'Error: [Thomas@novell.com] is not all lower case.') ]

        for curUser in users:
            email = curUser[0]
            password = curUser[1]
            name = curUser[2]
            msg = curUser[3]
            try:
                self.user.addUser(email, password, name)
                if (msg != ""):
                    self.assertEqual('Exception not raised!', email)
            except Exception, exc:
                self.assertEqual(str(exc), msg)

        # Check the file to make sure it's how it should be
        accountInfo = self.user._HtUserManagement__readInCsv()
        self.assertEqual(len(accountInfo), 3, "user_db is bigger than expected, expected 3, got " + str(len(accountInfo)))
        self.assertEqual(accountInfo[0], ["username","password","enc_password","full_name","been_notified"])
        self.assertEqual(accountInfo[1][0:2], ["rupert@novell.com", "mono"])
        self.assertEqual(accountInfo[1][3:],  ["Rupert Monkey","no"])
        self.assertEqual(accountInfo[2][0:2], ["rupert_monkey@novell.com", "onom"])
        self.assertEqual(accountInfo[2][3:],  ["Rupert Monkey 2","no"])


    def testConstructor(self):
        self.assertEqual(self.user.db_file, "/tmp/tmp_user.db")

    def testVerifyUsername(self):
        emails = [ ('Tho mas@novell.com','Error: [Tho mas@novell.com] is not a valid e-mail address.'),
                   ('thomas.com','Error: [thomas.com] is not a valid e-mail address.'),
                   ('thomas@novell','Error: [thomas@novell] is not a valid e-mail address.'),
                   ('Thomas@novell.com', 'Error: [Thomas@novell.com] is not all lower case.') ]

        for curEmail in emails:
            email = curEmail[0]
            msg = curEmail[1]
            try:

                self.user._HtUserManagement__verifyUsername(email)
                self.assertEqual('Exception not raised!', email)
            except Exception, exc:
                self.assertEqual(str(exc), msg)


if __name__ == '__main__':
    unittest.main()



# vim:ts=4:expandtab:
