NAME="osconfig-agent-test"
VERSION="0.1.0"
GOLANG="go1.12.1.linux-amd64.tar.gz"
GO=/tmp/go/bin/go
export GOPATH=/usr/share/gocode
export GOCACHE=/tmp/.cache

working_dir=${PWD}
if [[ $(basename "$working_dir") != $NAME ]]; then
  echo "Packaging scripts must be run from top of package dir."
  exit 1
fi

# Golang setup
[[ -d /tmp/go ]] && rm -rf /tmp/go
mkdir -p /tmp/go/
echo "Downloading Go"
curl -s "https://dl.google.com/go/${GOLANG}" -o /tmp/go/go.tar.gz
echo "Extracting Go"
tar -C /tmp/go/ --strip-components=1 -xf /tmp/go/go.tar.gz

echo "Pulling dependencies"
sudo su -c "GOPATH=${GOPATH} ${GO} get -d ./..."
sudo su -c "GOOS=windows GOPATH=${GOPATH} ${GO} get -d ./..."
