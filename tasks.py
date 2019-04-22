import os
import io
import datetime

from invoke import task
import docker


REGISTRY = "quay.io"
IMAGE_PREFIX = "xvello-images"


@task 
def build_all(ctx, tag="latest", autotag=True, push=True, nocache=False):
    images = [ f.name for f in os.scandir(".") if f.is_dir() and not f.name.startswith('.') ]
    _do_build(ctx, images, tag, autotag, push, nocache)


@task
def build(ctx, image, tag="latest", autotag=True, push=True, nocache=False):
    _do_build(ctx, [image], tag, autotag, push, nocache)


def _do_build(ctx, images, tag="latest", autotag=True, push=True, nocache=False, quiet=False):
    d = docker.from_env()

    if "DOCKER_PASSWORD" in os.environ:
        d.login(
            username=os.environ.get("DOCKER_USERNAME"),
            password=os.environ.get("DOCKER_PASSWORD"),
            registry=REGISTRY
            )

    weekly_tag = None
    if autotag:
        _, week, weekday = datetime.datetime.today().isocalendar()
        if weekday == 1:
            weekly_tag = 'week{:02d}'.format(week)

    for i in images:
        repo = "{}/{}/{}".format(REGISTRY, IMAGE_PREFIX, i)
        img = "{}:{}".format(repo, tag)
        if not quiet:
            print("Building {}".format(img))
        d.images.build(
            path=i,
            tag=img,
            nocache=nocache
            )
        if push:
            _push(d, img, quiet)
            if weekly_tag:
                d.api.tag(img, repo, weekly_tag)
                _push(d, "{}:{}".format(repo, weekly_tag), quiet)


def _push(client, image, quiet):
    if not quiet:
        print("Pushing {}".format(image))
    for line in client.images.push(image, stream=True, decode=True):
        if "error" in line:
            raise Exception(line)    