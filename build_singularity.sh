#!/bin/bash

set -e

if ! ver=$(git describe --tags --exact-match 2> /dev/null)
then
    ver=$(git rev-parse HEAD)
    ver=${ver:0:10}
fi
if ! git diff --quiet
then
    ver=${ver}-dirty
fi

TMPDIR=$(mktemp -d -p /tmp_disk)
export TMPDIR

dockerimg=localhost:5000/neck_removal-image:$ver
docker build -t $dockerimg .
docker push $dockerimg

SINGULARITY_TMPDIR=$(mktemp -d -p /tmp_disk)
export SINGULARITY_TMPDIR

export SINGULARITY_NOHTTPS=1
outimg=neck_removal-image-$ver.simg
if [ -e "$outimg" ]
then
	echo "$outimg already exists. exiting" >&2
	exit 1
fi
/opt/singularity/2.5.2/bin/singularity build "$outimg" docker://$dockerimg
rm -rf $TMPDIR
rm -rf $SINGULARITY_TMPDIR
