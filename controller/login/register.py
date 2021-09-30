def makeUser(self,name,pw,pw2,email):
        """Checking input is valid and not already exist in the current database before creating new user instance

        Args:
            name (string): username taken from user input, need to be more than 2 characters and less than 20 characters
            pw (string):  password taken from user input, need to be more than 8 character and less than 20 characters
            pw2 (string): confirm password, need to be identical with password input
            email (string): email from user, need to have @ and valid email name
        """
        self.destroy()
        pass