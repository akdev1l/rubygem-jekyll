srpm:
	dnf install -y rpkg
	rpkg srpm \
		--spec $(spec) \
		--with bootstrap \
		--outdir $(outdir)
	ls -l $(outdir) $(PWD)
