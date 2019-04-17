#! /bin/bash
version=$(cat osconfig-agent-test.goospec | sed -nE 's/.*"version":.*"(.+)".*/\1/p')
if [[ $? -ne 0 ]]; then
  echo "could not match version in goospec"
  exit 1
fi

GOOS=windows /tmp/go/bin/go build -ldflags "-X main.version=${version}" -o osconfig_agent_test.exe