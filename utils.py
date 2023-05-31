from jira import JIRA
from dotenv import load_dotenv
from os import environ

load_dotenv(".env")

OPTIONS = {"server": environ.get("server")}


class Jira:
    def __init__(self) -> None:
        self.jira = self.connect(OPTIONS)

    @staticmethod
    def connect(options) -> JIRA:
        return JIRA(options, basic_auth=(environ.get("username"), environ.get("pword")))

    def close(self) -> None:
        self.jira.close()

    def get_issue(self, jira_id) -> JIRA.issue:
        return self.jira.issue(jira_id)
