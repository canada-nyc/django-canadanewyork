#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

# if stdin is not a terminal, then keep it open
# because this means we are piping into this command and we need it open
docker run \
  $(if ! [ -t 0 ] ; then echo -i; fi) \
  --rm \
  --net=djangocanadanewyork \
  -e PGPASSWORD=${PGPASSWORD:-} \
  -e PGHOST=djangocanadanewyork_db_1 \
  -e PGUSER=postgres \
  postgres \
  ${@//localhost/djangocanadanewyork_db_1}
