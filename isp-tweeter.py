#!/usr/bin/env python3

from json import loads
from re import match
from subprocess import Popen
from sys import argv, exit
from tempfile import TemporaryDirectory
from tweepy import OAuthHandler, API

__version__ = "1.0.0"


def tweet(dload, uload, link, cfg):
    auth = OAuthHandler(cfg["ConsumerKey"], cfg["ConsumerSecret"])
    auth.set_access_token(cfg["AccessToken"], cfg["AccessSecret"])
    api = API(auth)

    if cfg["Debug"] == "True":
        api.update_status("This is a test tweet... %d Mbps download and %d Mbps upload. %s" % (dload, uload, link))
    else:
        update_status("Why do I pay for %s when I'm only getting %d Mbps download and %d Mbps upload? %s %s" % (cfg["DesiredSpeed"], dload, uload, cfg["TweetAt"], link))


if __name__ == "__main__":
    config = loads(open(argv[1]).read())
    if config["NeedsConfig"] == "True":
        exit("Please modify your config")

    with TemporaryDirectory() as tempdir:
        args = [config["DSLR-CLI"], "--ipv4", "--platform " + config["Platform"], "--latlong " + config["LatLong"], "-o json"]
        Popen(' '.join(args), shell=True, cwd=tempdir).wait()
        results = loads(open(tempdir + "/results.json").read())

    download = int(float(results["DownSpeed"].split()[0]))
    upload = int(float(results["UpSpeed"].split()[0]))
    if match('\d+', str(download)) and match('\d+', str(upload)):
        if download < 300 or upload < 300 or config["Debug"] == "True":
            tweet(download, upload, results["Url"], config)
