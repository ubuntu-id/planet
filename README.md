# Planet feed at Ubuntu-ID

## Who?

If you are using Ubuntu and want to share your blog, please let us know

## How to add my blog to planet?

You need to:
1. Create [Launchpad](https://launchpad.net) account
2. Sign [Ubuntu CoC](http://wiki.ubuntu-id.org/DokumentasiKomunitas/Tandatangan-CoC)
3. Create ticket/bug in [Ubuntu ID Launchpad page](https://bugs.launchpad.net/ubuntu-id-web/+filebug)
4. Inform what your full name and feed address
5. (optional) Hackergotchi if you want you face appear in planet

## etc
Planet Ubuntu ID is using planet venus and Ubuntu Theme, all copyrights
goes to origin creator

## How to install

We use Debian based distro for generating planet, you can build your own planet by following below tutorials:

### install requirement packages

```
apt install -y python-libxslt1 python-libxml2 python-genshi xsltproc python-django git python-lxml vim python-librdf nginx
```


### Copy planet venus and this repo

```
git clone https://github.com/rubys/venus/ /home/venus
git clone https://github.com/ubuntu-id/planet.git /home/venus/themes/ubuntu
```

### Generate planet and run nginx

To generate planet, you can execute below command

```
/usr/bin/python planet.py themes/ubuntu/config.ini
systemctl start nginx
```

The output directory is /usr/share/nginx/html, that's a default www directory for nginx. You can check from
browser http://localhost
