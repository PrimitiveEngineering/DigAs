import datetime


class Time:

    @staticmethod
    def get_current_time(time_format="%H:%M"):
        """
        Returns the current time: standard HH:MM
        :param time_format: (optional) (string)
        :return: current time (string)
        """

        now = datetime.datetime.now()
        return now.strftime(time_format)

    @staticmethod
    def get_current_date(date_format="%Y/%m/%d"):
        """
        Returns the current time: standard YYYY/mm/dd
        :param date_format: (optional) (string)
        :return: current date (string)
        """

        now = datetime.datetime.now()
        return now.strftime(date_format)

    @staticmethod
    def get_current_date_time(date_time_format="%Y/%m/%d %H:%M"):
        """
        Returns the current date and time: standard YYYY/MM/DD HH:MM
        :return: current date time (string)
        """

        now = datetime.datetime.now()
        return now.strftime(date_time_format)

    @staticmethod
    def change_time_format(date_time):
        """
        Returns the time in the format HH:MM
        :param date: date_time (string)
        :return: YYYY/MM/DD (string)
        """
        date_obj = datetime.datetime.strptime(date_time, "%Y/%m/%d %H:%M:%S")
        return date_obj.strftime('%H:%M')
    @staticmethod
    def change_date_format_t2s(date, date_format):
        """
        Returns the date in the S2T format YYYY/MM/DD
        :param date: date (string)
        :param date_format: the current format of the date (string)
        :return: YYYY/MM/DD (string)
        """

        date_obj = datetime.datetime.strptime(date, date_format)
        return date_obj.strftime('%Y/%m/%d')

    @staticmethod
    def change_date_time_format_t2s(date_time, date_time_format):
        """
        Returns the date in the S2T format YYYY/MM/DD HH:MM
        :param date_time: date and time (string)
        :param date_time_format:the current format of the date and time (string)
        :return: YYYY/MM/DD HH:MM (string)
        """

        date_obj = datetime.datetime.strptime(date_time, date_time_format)
        return date_obj.strftime('%Y/%m/%d %H:%M')

    @staticmethod
    def split_date_time(date_time, date_time_format="%Y/%m/%d %H:%M"):
        """
        Splits the date and time
        :param date_time: (string)
        :param date_time_format: (optional) (string)
        :return: YYYY/MM/DD (string), HH:MM (string)
        """

        date_obj = datetime.datetime.strptime(date_time, date_time_format)
        return date_obj.strftime('%Y/%m/%d'), date_obj.strftime('%H:%M')
