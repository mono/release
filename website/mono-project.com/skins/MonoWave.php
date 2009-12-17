<?php
/**
 * MonoWave
 *
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */

if( !defined( 'MEDIAWIKI' ) )
	die();


/** */
require_once('includes/SkinTemplate.php');

/*
if($this->data['lastmod'   ]) { ?><div id="f-lastmod"><?php    $this->html('lastmod')    ?></div> } 
if($this->data['viewcount' ] && $userLoggedIn) { ?><div id="f-viewcount"><?php  $this->html('viewcount')  ?></div> }
*/
/**
 * Inherit main code from SkinTemplate, set the CSS and template filter.
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */
class SkinMonoWave extends SkinTemplate {
	/** Using monoproject. */
	function initPage( &$out ) {
		SkinTemplate::initPage( $out );
		$this->skinname  = 'MonoWave';
		$this->stylename = 'MonoWave';
		$this->template  = 'MonoWaveTemplate';
	}
}
	
class MonoWaveTemplate extends QuickTemplate {

    var $url_prefix = "http://mono-project.com";

    function get_menu_url ($url)
    {
        return $url[0] == "/" ? "$this->url_prefix${url}" : $url;
    }
	 
	function execute() {
	    $template_page = $this->data['thispage'] == "TemplateExport";
    	$home_page = $this->data['thispage'] == "Main_Page" || $this->data['thispage'] == "NothingToSeeHere";
    	$wide = ' class="wide"';
	
?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php $this->text('lang') ?>" lang="<?php $this->text('lang') ?>" dir="<?php $this->text('dir') ?>">
  <head>
    <meta http-equiv="Content-Type" content="<?php $this->text('mimetype') ?>; charset=<?php $this->text('charset') ?>" />
    <?php $this->html('headlinks') ?>
    <title><?php if (!$template_page) { $this->html('pagetitle'); } ?></title>
    <link rel="alternate" type="application/rss+xml" title="RSS" href="<?php echo $this->url_prefix?>/news/index.rss2"/>
    <link rel="stylesheet" type="text/css" media="print" href="<?php echo $this->url_prefix?><?php $this->text('stylepath') ?>/common/commonPrint.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/screen.css" />
    <script type="text/javascript" src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/prototype.js"></script>
    <script type="text/javascript" src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/wikihacks.js"></script>
    <script type="text/javascript" src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/common/wikibits.js"></script>
    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"> </script>
    <script type="text/javascript">
        _uacct = "UA-76510-1";
        urchinTracker();
    </script>
  </head>
  <body <?php echo 'id="page-'.htmlspecialchars(preg_replace("/( |:)/","",$this->data['title'])).'"'; ?> class="<?php if($this->data['nsclass']) { ?><?php $this->text('nsclass') ?><?php } ?>">
    <?php 
        $i = "";
        $navlist = "";

        foreach ($this->data['personal_urls'] as $key => $item) {
            $i++;
            $navlist .= '<li><a href="'.htmlspecialchars($item['href']).'"';
            if(!empty($item['class'])) { 
                $navlist .= ' class="'.htmlspecialchars($item['class']).'"'; 
            } 
            $navlist .= '>';
            $navlist .= htmlspecialchars($item['text']).'</a></li> ';
        }
        
        // Hack to work-around broken MediaWiki stuff... 
        if (!ereg("Special:Userlogin",$navlist) || (!$this->data['personal_urls'])) {
            $userLoggedIn = true;
        }
        
        if ($userLoggedIn) {
            echo "<!--BEGIN USER UTILITY BAR-->\n";
            echo '<div id="utility-bar">';
            echo '<div id="utility-bar-toggle"><a href="javascript:void(0)" id="utility-bar-toggle-link">&nbsp;</a></div>';
            echo '<div id="utility-bar-contents">';
            echo '<div class="portlet" id="p-personal"><ul>';
            echo $navlist;
            echo '</ul></div>';
    ?>
	<div id="p-cactions" class="portlet">
      <h4>Views:</h4>
	  <ul>
	    <?php foreach($this->data['content_actions'] as $key => $action) {
	       ?><li id="ca-<?php echo htmlspecialchars($key) ?>"
	       <?php if($action['class']) { ?>class="<?php echo htmlspecialchars($action['class']) ?>"<?php } ?>
	       ><a href="<?php echo htmlspecialchars($action['href']) ?>"><?php
	       echo htmlspecialchars($action['text']) ?></a></li><?php
	     } ?>
	  </ul>
	</div>
	<div class="portlet" id="p-tb">
      <h4><?php $this->msg('toolbox') ?>:</h4>
	    <ul>
		  <?php if($this->data['notspecialpage']) { foreach( array( 'recentchanges', 'whatlinkshere', 'recentchangeslinked' ) as $special ) { ?>
		  <li id="t-<?php echo $special?>"><a href="<?php
		    echo htmlspecialchars($this->data['nav_urls'][$special]['href']) 
		    ?>"><?php echo $this->msg($special) ?></a></li>
		  <?php } } ?>
	      <?php if($this->data['feeds']) { ?><li id="feedlinks"><?php foreach($this->data['feeds'] as $key => $feed) {
	        ?><span id="feed-<?php echo htmlspecialchars($key) ?>"><a href="<?php
	        echo htmlspecialchars($feed['href']) ?>"><?php echo htmlspecialchars($feed['text'])?></a>&nbsp;</span>
	        <?php } ?></li><?php } ?>
	      <?php foreach( array('contributions', 'emailuser', 'upload', 'specialpages') as $special ) { ?>
	      <?php if($this->data['nav_urls'][$special]) {?><li id="t-<?php echo $special ?>"><a href="<?php
	        echo htmlspecialchars($this->data['nav_urls'][$special]['href'])
	        ?>"><?php $this->msg($special) ?></a></li><?php } ?>
	      <?php } ?>
	    </ul>
	</div>
	<?php if( $this->data['language_urls'] ) { ?><div id="p-lang" class="portlet">
	  <h4><?php $this->msg('otherlanguages') ?></h4>
	  <div class="pBody">
	    <ul>
	      <?php foreach($this->data['language_urls'] as $langlink) { ?>
	      <li>
	      <a href="<?php echo htmlspecialchars($langlink['href'])
	        ?>"><?php echo $langlink['text'] ?></a>
	      </li>
	      <?php } ?>
	    </ul>
	  </div>
      </div>
      <?php 
          } 
          echo "</div></div>\n";
          echo "<!--END USER UTILITY BAR-->\n";
      } 
    ?>

<div id="page">
  <div id="tl"></div>
  <div id="tr"></div>
  <div id="header">
    <h1>Mono</h1>    
    <a href="http://mono-project.com/" title="Mono"><div id="mono-logo"></div></a>
    <ul>
    <?php
        $selected_href = "/Start";
        foreach($this->data['navigation_urls'] as $navlink) {
            $href = "/".$this->data['thispage'];
            if ($navlink['href'] == $href) {
                $selected_href = $href;
            }
        }
        
        foreach($this->data['navigation_urls'] as $navlink) { ?>
      <li <?php if ($navlink['href'] == $selected_href) { ?>class="current_page_item"<?php } ?> id="menu-<?php echo htmlspecialchars($navlink['id'])?>"><a href="<?php echo $this->get_menu_url ($navlink['href']); ?>"><?php echo htmlspecialchars($navlink['text']) ?></a></li>
<?php } ?>
    </ul>
    <div id="search">
      <form method="get" action="http://www.google.com/search?">
        <div>
          <input type="hidden" value="www.mono-project.com" id="sitesearch" name="sitesearch" />
          <input type="hidden" value="www.mono-project.com" id="domains" name="domains" />
          <input class="text" name="q" id="q" type="text" value="Search Mono" 
            onblur="if (this.value == '') this.value='Search Mono';" 
            onfocus="if (this.value == 'Search Mono') this.value='';" />
          <input class="button" type="submit" value="Go" />
        </div>
      </form>
    </div>
  </div>
  <?php if ($home_page) { ?>
  <?php } else { ?>
  <div id="content-header"><h2><!--BEGIN PAGE TITLE--><?php if (!$template_page) { $this->html('title'); } ?><!--END PAGE TITLE--></h2></div>
  <div style="height:50px; background-image:url(<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-bg-blue-bar.png);width:100%;"></div>
  <?php } ?>
  <div id="wrapper"<?php echo $wide?>>
<?php if ($home_page) { ?>
    
    <div id="home-intro">
      <div id="home-intro-banner">
        <table><tr>
          <td class="square"><div class="home-caption">Mono</div><div><img src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-thumb-mono.png" style="float: right;padding-right:10px;padding-top:3px;"></div>
          <div class="home-content">An open source, cross-platform, implementation of C# and the CLR that is binary compatible with Microsoft.NET</div>
          <a class="download" href="/Download">Download</a>
          <a class="learn" href="/Start">Learn More</a>
          </td>
          <td></td>
          <td class="square"><div class="home-caption">MonoDevelop</div><div><img src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-thumb-md.png" style="float: right;padding-right:8px;padding-top:5px;"></div>
          <div class="home-content">An open Source C# and .NET development environment for Linux, Windows, and Mac OS X</div>
          <a class="download" href="http://monodevelop.com/Download">Download</a>
          <a class="learn" href="http://monodevelop.com/">Learn More</a>
          </td>
          <td></td>
          <td class="square"><div class="home-caption">Moonlight</div><div><img src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-thumb-moonlight.png" style="float: right;padding-right:5px;padding-top:3px;"></div>
          <div class="home-content">An open source implementation of Microsoft Silverlight for Linux and other Unix/X11 based operating systems</div>
          <a class="download" href="http://www.go-mono.com/moonlight/">Download</a>
          <a class="learn" href="http://mono-project.com/Moonlight">Learn More</a>
          </td>
          </tr></table>
      </div>
      <div id="home-sub-banner">
        <table><tr>
          <td class="square"><div class="home-caption">Mono Tools for<br/> Visual Studio</div><div><img src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-thumb-monovs.png" style="float: right;padding-right:12px;padding-top:3px;"></div>
          <div class="home-content">Develop and migrate .NET applications to Mono on Linux without leaving Visual Studio</div>
          <a class="try" href="http://go-mono.com/monovs/download/">Try</a><br/>
          <a class="buy" href="/Store">Buy</a>
          <a class="learn" href="http://go-mono.com/monovs/">Learn More</a>
          </td>
          <td></td>
          <td class="square"><div class="home-caption">SUSE Linux Enterprise Mono Extension</div><div><img src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-thumb-geeko.png" style="float: right;padding-right:4px;padding-top:8px;"></div>
          <div class="home-content">Run .NET applications, including ASP.NET, ASP.NET AJAX, and ASP.NET MVC, commercially supported on SUSE Linux Enterprise Server</div>
          <a class="try" href="http://www.novell.com/products/mono/eval.html">Try</a><br/>
          <a class="buy" href="http://www.novell.com/products/mono/howtobuy.html">Buy</a>
          <a class="learn" href="http://www.novell.com/products/mono/">Learn More</a>
          </td>
          <td></td>
          <td class="square"><div class="home-caption">MonoTouch</div><div><img src="<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mp-thumb-iphone.png" style="float: right;padding-right:15px;padding-top:2px;"></div>
          <div class="home-content">Create C# and .NET apps for iPhone and iPod Touch, while taking advantage of iPhone APIs, and reusing existing .NET code, libraries, and skills</div>
          <a class="try" href="http://monotouch.net/DownloadTrial">Try</a><br/>
          <a class="buy" href="http://monotouch.net/Store">Buy</a>
          <a class="learn" href="http://monotouch.net/">Learn More</a>
          </div>
          </td>
          </tr></table>
      </div>
    </div>
<?php } ?>
    <div id="sidebar">
    <div id="toc-parent"></div>
    <!-- BEGIN SIDE CONTENT -->
    
    
    <!-- END SIDE CONTENT -->
    </div>
    <div id="content"<?php echo $wide?>>
    <!-- BEGIN MAIN CONTENT -->


<?php $this->html('bodytext') ?>


    <!-- END MAIN CONTENT -->
    </div><!--#content-->
    
    <div id="footer">
                    <ul id="footer-menu">
                        <li><a href="http://www.novell.com/linux"><div id="novell-logo"></div></a>
                            <ul>
                                <li style="margin-top: 15px;"><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/">
                                <div id="by-sa"></div></a></li>
                                <li><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/us/">
                                <div id="by-nc-nd"></div></a></li>
                                <li><a href="/Legal">Legal Notices</a></li>
                                <li>          
<?php if(!$userLoggedIn) { 
	      if ($this->data['personal_urls']['login']) {
		      $loginvar="login";
	      } else {
		      $loginvar="anonlogin";
	      }
              echo '<a href="'.htmlspecialchars($this->data['personal_urls'][$loginvar]['href']).'">'.
              htmlspecialchars($this->data['personal_urls'][$loginvar]['text']).'</a>';
              //print_r($this->data['personal_urls'][$loginvar]);
		}
?>
                           </li>
                            </ul>
                        </li>
                        <li>Mono
                            <ul>
                                <li><a href="/About">About</a></li>
                                <li><a href="/Roadmap">Roadmap</a></li>
                                <li><a href="/Plans">Technologies</a></li>
                                <li><a href="/Screenshots">Screenshots</a></li>
                                <li><a href="/FAQ:_General">FAQ</a></li>
                                <li><a href="/Contact">Contact</a></li>
                            </ul>
                        </li>
                        <li>Download
                          <ul>
                              <li><a href="http://www.go-mono.com/mono-downloads/download.html">Latest Release</a></li>
                              <li><a href="http://mono.ximian.com/daily/">Daily Snapshots</a></li>
                              <li><a href="http://www.mono-project.com/OldReleases">Previous Releases</a></li>
                              <li><a href="http://monodevelop.com/Download">MonoDevelop</a></li>
                              <li><a href="http://www.mono-project.com/MoMA">Mono Migration Analyzer</a></li>
                              <li><a href="http://www.go-mono.com/moonlight/">Moonlight</a></li>
                              <li><a href="http://www.go-mono.com/monovs/download">Mono Tools for Visual Studio</a></li>
                              <li><a href="http://monotouch.net/DownloadTrial">MonoTouch</a></li>
                              <li><a href="http://www.novell.com/products/mono/eval.html">SUSE Linux Enterprise<br/>Edition Mono Extension</a></li>
                          </ul>
                      </li>
                        <li>Documentation
                            <ul>
                                <li><a href="/Start">Getting Started</a></li>
                                <li><a href="http://www.go-mono.com/docs/">API Reference</a></li>
                                <li><a href="/Articles">Articles</a></li>
                            </ul>
                        </li>
                        <li>Community
                            <ul>
                                <li><a href="/Mailing_Lists">Mailing Lists</a></li>
                                <li><a href="http://www.go-mono.com/forums">Forums</a></li>
                                <li><a href="/IRC" class="external">Chat/IRC</a></li>
                                <li><a href="http://www.go-mono.com/monologue">Blogs</a></li>
                            </ul>
                        </li>
                        <li>Contribute
                            <ul>
                                <li><a href="/Contributing">Contributing Guide</a></li>
                                <li><a href="/Bugs">Report Bugs</a></li>
                                <li><a href="/SVN">SVN</a></li>
                                <li><a href="http://mono.ximian.com/monobuild/">Build Status</a></li>
                                <li><a href="http://go-mono.com/status/">Class Status</a></li>

                            </ul>
                        </li>
                    </ul>
                <div style="clear: both;"></div>
    </div>
    
  </div><!--#wrapper-->
</div><!--#page-->

</body>
</html>


<?php /*

<div id="globalWrapper">
    <div id="bigWrapper">

	<div class="portlet" id="p-logo">
	  <a href="<?php echo htmlspecialchars($this->data['nav_urls']['mainpage']['href'])?>"
	    title="<?php $this->msg('mainpage') ?>"></a>
	</div>

      <div id="column-content">
	<div id="content">
	  <div id="bodyContent">
      <h3 id="siteSub">
        <?php $this->msg('tagline') ?>
      </h3>
      <div id="menu">
        <ul>
          <li>
            <span class="heading">About</span>
            <ul>
              <li>
                <a href="/About_Mono">About Mono</a>
              </li>
              <li>
                <a href="/Mono_Project_Roadmap">Roadmap</a>
              </li>
              <li>
                <a href="/Plans">Technologies</a>
              </li>
              <li>
                <a href="/Screenshots">Screenshots</a>
              </li>
              <li>
                <a href="/FAQ:_General">FAQs</a>
              </li>
              <li>
                <a href="http://www.mono-project.com/Contact">Contact</a>
              </li>
            </ul>
          </li>
          <li>Download
              <ul>
                  <li><a href="http://www.go-mono.com/mono-downloads/download.html">Latest Release</a></li>
                  <li><a href="http://mono.ximian.com/daily/">Daily Snapshots</a></li>
                  <li><a href="http://www.mono-project.com/OldReleases">Previous Releases</a></li>
                  <li><a href="http://monodevelop.com/Download">MonoDevelop</a></li>
                  <li><a href="http://www.mono-project.com/MoMA">Mono Migration Analyzer</a></li>
                  <li><a href="http://www.go-mono.com/moonlight/">Moonlight</a></li>
                  <li><a href="http://www.go-mono.com/monovs/download">Mono Tools for Visual Studio</a></li>
                  <li><a href="http://monotouch.net/DownloadTrial">MonoTouch</a></li>
                  <li><a href="http://www.novell.com/products/mono/eval.html">SUSE Linux Enterprise<br/>Edition Mono Extension</a></li>
              </ul>
          </li>
          <li>
            <span class="heading">Documentation</span>
            <ul>
              <li>
                <a href="/Start">Getting Started</a>
              </li>
              <li>
                <a href="http://www.go-mono.com/docs/">API Reference</a>
              </li>
              <li>
                <a href="/Articles">Articles</a>
              </li>
            </ul>
          </li>
          <li>Community
              <ul>
                  <li><a href="http://www.mono-project.com/Mailing_Lists">Mailing Lists</a></li>
                  <li><a href="http://www.go-mono.com/forums">Forums</a></li>
                  <li><a href="http://www.mono-project.com/IRC" class="external">Chat/IRC</a></li>
                  <li><a href="http://www.go-mono.com/monologue">Blogs</a></li>
              </ul>
          </li>
          <li>Contribute
              <ul>
                  <li><a href="http://www.mono-project.com/Contributing">Contributing Guide</a></li>
                  <li><a href="http://www.mono-project.com/Bugs">Report Bugs</a></li>
                  <li><a href="http://www.mono-project.com/SVN">SVN</a></li>
                  <li><a href="http://mono.ximian.com/monobuild/">Build Status</a></li>
                  <li><a href="http://go-mono.com/status/">Class Status</a></li>

              </ul>
          </li>
        </ul>
        <br />
        <div style="text-align: center">
          <a href="http://www.gnu.org/copyleft/fdl.html">
            <img src="skins/<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/gnu-fdl.png" alt="GNU Free Documentation License 1.2 (only text)" />
          </a>
          <br />
          <div id="f-poweredbyico" style="clear: both;">
            <a href="http://www.mediawiki.org/">
              <img src="skins/<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/mediawiki-tiny.png" alt="MediaWiki" />MediaWiki
            </a>
          </div>
        </div>
        <?php if(!$userLoggedIn) { 
	      if ($this->data['personal_urls']['login']) {
		      $loginvar="login";
	      } else {
		      $loginvar="anonlogin";
	      }
              echo '<div id="f-login"><a href="'.htmlspecialchars($this->data['personal_urls'][$loginvar]['href']).'">'.
              htmlspecialchars($this->data['personal_urls'][$loginvar]['text']).'</a>'.'</div>';
              //print_r($this->data['personal_urls'][$loginvar]);
		}
      ?>      </div>
      <div id="contentSub">
        <?php $this->html('subtitle') ?>
      </div>
      <?php if($this->data['undelete']) { ?>
      <div id="contentSub">
        <?php     $this->html('undelete') ?>
      </div>
      <?php } ?>
      <?php if($this->data['newtalk'] ) { ?>
      <div class="usermessage">
        <?php $this->html('newtalk')  ?>
      </div>
      <?php } ?>
      <div class="content-half">

        <!-- start content -->
        <?php if($this->data['sitenotice']) { ?>
        <div id="siteNotice">
          <?php $this->html('sitenotice') ?>
        </div>
        <?php } ?>
        <?php
          if ($this->data['title'] != 'Main Page') {
              echo '<h1 class="firstHeading">'.htmlspecialchars($this->data['title']).'</h1>';
          }
      ?>
        <?php $this->html('bodytext') ?>
        <?php if($this->data['catlinks']) { ?>
        <div id="catlinks">
          <?php       $this->html('catlinks') ?>
        </div>
        <?php } ?>
        <!-- end content -->
        <div class="visualClear"></div>
      </div>
	  </div>
	</div>
      </div>

      <div id="quicklinks">
        <a href="/Screenshots">
          <img alt="screenshots" src="skins/<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/images.png" /> Screenshots
        </a> |
        <a href="/Downloads">
          <img alt="Downloads" src="skins/<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/package_go.png" /> Downloads
        </a> |
        <a href="http://www.go-mono.com/docs/">
          <img alt="Documentation" src="skins/<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/report.png" /> Documentation
        </a> |
        <a href="http://www.go-mono.com/monologue/">
          <img alt="Blogs" src="skins/<?php echo $this->url_prefix?><?php $this->text('stylepath' )?>/<?php $this->text('stylename' )?>/images/comments.png" /> Blogs
        </a>
      </div>

      <div id="searchbox">
        <form name="searchform" action="/Special:Search" id="searchform">
          <input id="searchInput" name="search" accesskey="f" value="" type="text" />
          <input name="go" class="searchButton" id="searchGoButton" value="Search" type="submit" />
        </form>
      </div>
      <div id="footer">
      </div>
      </div>
    </div>
    <?php $this->html('reporttime') ?>
  </body>
</html>*/?>


<?php
	}
}

?>
