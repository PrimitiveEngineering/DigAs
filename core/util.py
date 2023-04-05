class Speech2TextUtil:
    """
    Some utilities for Speech2Text
    """

    def user_termination_desired(self, user_input):
        """
        Checks if user wants to terminate the current use case
        :param user_input: s2t input
        :return: boolean if user wants to cancel the current action
        """

        user_input = str(user_input).lower()

        if any(element in user_input for element in ["cancel", "terminate"]):
            return True
        else:
            return False

    def user_input_func(self, s2t, t2s):
        """
        Starts user input and evaluates input and termination desire.
        :param s2t: Speech2Text sevice
        :param t2s: Text2Speech service
        :return: speech input (string) and termination desire (boolean).
        """
        user_input = None
        user_valid_input = False

        # do while loop: param user_valid_input
        while True:
            user_input, user_valid_input = s2t.trigger()
            if user_valid_input:
                break
            t2s.trigger("Sorry. I couldn't understand you. Can you repeat that please", False)

        print(user_input)

        if self.user_termination_desired(user_input):
            return (None, True)

        return (user_input, False)
