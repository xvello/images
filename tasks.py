import os
import io
import datetime

from invoke import task
import docker


REGISTRY = "quay.io"
IMAGE_PREFIX = "xvello-images"


class SimpleDocker(object):
    def __init__(self, organization, registry="docker.io"):
        self.client = docker.from_env()
        self.registry = registry
        self.org = organization

        if "DOCKER_PASSWORD" in os.environ:
            self.client.login(
                username=os.environ.get("DOCKER_USERNAME"),
                password=os.environ.get("DOCKER_PASSWORD"),
                registry=registry,
            )

    def build_path(self, image, tag=None):
        path = "{}/{}/{}".format(self.registry, self.org, image)
        if tag:
            path = "{}:{}".format(path, tag)
        return path

    def build(self, folder, image, tag, nocache=False, quiet=False):
        path = self.build_path(image, tag)
        if not quiet:
            print("Building {}".format(path))
        self.client.images.build(path=folder, tag=path, nocache=nocache, rm=True)

    def push(self, image, tag, quiet=False):
        path = self.build_path(image, tag)
        if not quiet:
            print("Pushing  {}".format(path))
        for line in self.client.images.push(path, stream=True, decode=True):
            if "error" in line:
                raise Exception(line)

    def retag(self, image, old_tag, new_tag):
        self.client.api.tag(
            self.build_path(image, old_tag),
            self.build_path(image),
            new_tag,
            force=True
        )


@task
def build_all(ctx, tag="latest", autotag=True, push=True, nocache=False):
    images = [
        f.name for f in os.scandir(".") if f.is_dir() and not f.name.startswith(".")
    ]
    _do_build(ctx, images, tag, autotag, push, nocache)


@task
def build(ctx, image, tag="latest", autotag=True, push=True, nocache=False):
    _do_build(ctx, [image], tag, autotag, push, nocache)


def _do_build(ctx, images, tag="latest", autotag=True, push=True, nocache=False):
    weekly_tag = None
    if autotag:
        _, week, weekday = datetime.datetime.today().isocalendar()
        if weekday == 1:
            weekly_tag = "week{:02d}".format(week)

    d = SimpleDocker(IMAGE_PREFIX, REGISTRY)
    for i in images:
        d.build(i, i, tag, nocache)
        if push:
            d.push(i, tag)
            if weekly_tag:
                d.retag(i, tag, weekly_tag)
                d.push(i, weekly_tag)
