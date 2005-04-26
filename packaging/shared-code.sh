function distro_info () {
	DISTRO=$1
	
	case "$DISTRO" in
		*-i[35]86) ARCH=x86 ;;
		 *-x86_64) ARCH=x86_64 ;;
	esac
	
	case "$DISTRO" in
		fedora-* | redhat-*        ) DISTRO_TYPE=redhat;;
		suse-*   | nld-* | sles-*  ) DISTRO_TYPE=suse;;
	esac
	
	case "$DISTRO" in
		rhel-3-i386 )
			DISTRO_ALIASES=(
				rhel-3as-i386
				rhel-3ws-i386
				rhel-3es-i386
			)
		;;
		
		rhel-4-i386 )
			DISTRO_ALIASES=(
				rhel-4as-i386
				rhel-4ws-i386
				rhel-4es-i386
			)
		;;
		
		* )
			DISTRO_ALIASES=()
		;;
	esac
}

function ships_package ()
{

	for i in ${USE_HOSTS[@]}; do
		[[ $i == $DISTRO ]] && return 0
	done
	
	return 1
}

function latest_version ()
{
	[ "x$1" == x ] && return 1
	
	LATEST_VERSION=`ls -d -t -1  $* | head -n1`
	return 0
}