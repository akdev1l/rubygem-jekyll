srpm:
	dnf install -y rpkg
	rpkg srpm --with bootstrap --outdir $(outdir)
	cp *.patch *.gem *.tar.gz $(outdir)/
