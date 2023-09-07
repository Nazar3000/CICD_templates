import argparse
import logging
import os
import sys

from atlassian.bitbucket.cloud import BitbucketCloudBase
from atlassian.bitbucket.cloud import Repositories

FAST_FORWARD_ERROR_TPL = "Unable to fast forward due changes in destination branch."
PULLREQUEST_ERROR_TPL = "There are no changes to be pulled"
DEFAULT_MERGE_STRATEGY = "fast_forward"


class Cloud(BitbucketCloudBase):
    def __init__(self, url="https://api.bitbucket.org/", *args, **kwargs):
        kwargs["cloud"] = True
        kwargs["api_root"] = None
        kwargs["api_version"] = "2.0"
        url = url.strip("/") + "/{}".format(kwargs["api_version"])
        super().__init__(url, *args, **kwargs)
        self.__repositories = Repositories(f"{self.url}/repositories", **{**self._new_session_args, **kwargs})

    @property
    def repositories(self):
        return self.__repositories


def get_json_from_response(response):
    try:
        return response.json()
    except Exception as e:
        logging.exception(f"Error: {e} when parsing JSON response with content:{response.content}")

        raise


def get_client():
    return Cloud(username=os.getenv("APP_USER"), password=os.getenv("APP_PASSWORD"), advanced_mode=True)


def open_pullrequest(args):
    client = get_client()
    data = {
        "description": "Automatic pull request created.",
        "state": "OPEN",
        "title": f"Auto Merge: {args.source} -> {args.destination}",
        "source": {"branch": {"name": args.source}},
        "destination": {"branch": {"name": args.destination}},
    }

    response = client.repositories.post(os.path.join(args.repo_owner, args.repo_slug, "pullrequests"), data=data)
    return get_json_from_response(response)


def get_merge_pullrequest_data(merge_strategy=DEFAULT_MERGE_STRATEGY):
    return {"close_source_branch": False, "merge_strategy": merge_strategy}


def get_response_error_message(response):
    return response.get("error", {}).get("message")


def merge_pullrequest(args, pullrequest):
    merge_url = pullrequest["links"]["merge"]["href"]
    data = get_merge_pullrequest_data()
    client = get_client()
    merge_path = os.path.join(args.repo_owner, args.repo_slug, *merge_url.split("/")[-3:])
    fast_forward_merge_response = get_json_from_response(client.repositories.post(merge_path, json=data))
    fast_forward_merge_error = get_response_error_message(fast_forward_merge_response)
    if fast_forward_merge_error == FAST_FORWARD_ERROR_TPL:
        data = get_merge_pullrequest_data(merge_strategy="merge_commit")
        merge_commit_response = get_json_from_response(client.repositories.post(merge_path, json=data))
        merge_commit_error = get_response_error_message(merge_commit_response)
        logging.warning(merge_commit_response)
        if not merge_commit_error:
            sys.exit(0)
        else:
            sys.exit(9)
    elif not fast_forward_merge_error:
        logging.warning(fast_forward_merge_response)
        sys.exit(0)
    else:
        logging.warning(fast_forward_merge_response)
        sys.exit(9)


def automerge_main(args):
    pullrequest_response = open_pullrequest(args)
    pullrequest_response_error = get_response_error_message(pullrequest_response)
    if pullrequest_response_error == PULLREQUEST_ERROR_TPL:
        logging.warning(pullrequest_response_error)
        sys.exit(0)
    elif not pullrequest_response_error:
        merge_pullrequest(args, pullrequest_response)
    else:
        logging.warning(pullrequest_response_error)
        sys.exit(9)


def get_arguments():
    parser = argparse.ArgumentParser(description="Django_optimz automerge script")
    parser.add_argument("-s", "--source", dest="source", required=True)
    parser.add_argument("-d", "--destination", dest="destination", required=True)
    parser.add_argument("--repo-owner", dest="repo_owner", required=True)
    parser.add_argument("--repo-slug", dest="repo_slug", required=True)
    parsed_args = parser.parse_args()
    return parsed_args


if __name__ == "__main__":
    arguments = get_arguments()
    automerge_main(arguments)
