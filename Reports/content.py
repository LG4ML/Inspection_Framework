import abc
from matplotlib.figure import Figure
import pandas as pd


class Content(abc.ABC):
    """
    The base class for all content types. This class is abstract and cannot be instantiated. It is used to define the
    interface for all content types. All content types must implement the render method. The render method is called
    by the report to generate the content for the report.
    """
    def __init__(self, key: str, content):
        """
        The constructor for the Content class.

        :param key: The key for the content.
        """
        self.__key = key
        self.__content = content

    @property
    def key(self):
        """
        The key property for the content.

        :return: The key for the content.
        """
        return self.__key

    @property
    def content_type(self):
        """
        The property for the content type.

        :return: The content_type for the content.
        """
        return type(self.__content)

    @property
    def content(self):
        """
        The property for the content.

        :return:
        """
        return self.__content

    @abc.abstractmethod
    def render(self, report, **kwargs):
        """
        This method is called by the report to generate the content for the report.

        :param report: The report object.
        :param kwargs: Additional keyword arguments.
        :return: The content for the report.
        """
        pass


class TextContent(Content):
    """
    The TextContent class is used to add text content to a report.
    """
    def __init__(self, key: str, text: str):
        """
        The constructor for the TextContent class.

        :param key: The key for the content.
        :param text: The text for the content.
        """
        super().__init__(key, text)

    def render(self, report, **kwargs):
        pass


class FigureContent(Content):
    """
    The FigureContent class is used to add figure content to a report.
    """
    def __init__(self, key: str, figure: Figure):
        """
        The constructor for the FigureContent class.

        :param key: The key for the content.
        :param figure: The figure for the content.
        """
        super().__init__(key, figure)

    def render(self, report, **kwargs):
        pass


class DataFrameContent(Content):
    """
    The DataFrameContent class is used to add data frame content to a report.
    """
    def __init__(self, key: str, data_frame: pd.DataFrame):
        """
        The constructor for the DataFrameContent class.

        :param key: The key for the content.
        :param data_frame: The data frame for the content.
        """
        super().__init__(key, data_frame)

    def render(self, report, **kwargs):
        pass
