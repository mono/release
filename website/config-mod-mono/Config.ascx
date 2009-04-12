<%@ Control 
    Language="C#" 
    AutoEventWireup="true" 
    CodeBehind="Config.ascx.cs" 
    Inherits="ModMonoConfig.Config" %><% 
if (this.IsVirtualHost) {
%><VirtualHost *:80>
  ServerName <%= this.ServerName %><%= this.FormattedServerAliases() %><% if (!string.IsNullOrEmpty(ServerAdmin)) { %>
  ServerAdmin <%= this.ServerAdmin %><% } %>
  DocumentRoot <%= this.DocumentRoot %><%
} else { 
%>  Alias /<%= this.ApplicationName %> "<%= this.DocumentRoot %>"<%
} %>
  # MonoServerPath can be changed to specify which version of ASP.NET is hosted
  # mod-mono-server1 = ASP.NET 1.1 / mod-mono-server2 = ASP.NET 2.0
  # For SUSE Linux Enterprise Mono Extension, uncomment the line below:
  # MonoServerPath <%= this.MonoServerAlias %> "/opt/novell/mono/bin/mod-mono-server2"
  # For Mono on openSUSE, uncomment the line below instead:
  MonoServerPath <%= this.MonoServerAlias %> "/usr/bin/mod-mono-server2"

  # To obtain line numbers in stack traces you need to do two things: 
  # 1) Enable Debug code generation in your page by using the Debug="true" 
  #    page directive, or by setting <compilation debug="true" /> in the 
  #    application's Web.config
  # 2) Uncomment the MonoDebug true directive below to enable mod_mono debugging
  <% if (!this.EnableDebug) { %># <% } %>MonoDebug <%= this.MonoServerAlias %> true
  
  # The MONO_IOMAP environment variable can be configured to provide platform abstraction
  # for file access in Linux.  Valid values for MONO_IOMAP are:
  #    case
  #    drive
  #    all
  # Uncomment the line below to alter file access behavior for the configured application
  <% if (!this.EnablePlatformAbstraction) { %># <% } %>MonoSetEnv <%= this.MonoServerAlias %> MONO_IOMAP=all
  #
  # Additional environtment variables can be set for this server instance using 
  # the MonoSetEnv directive.  MonoSetEnv takes a string of 'name=value' pairs 
  # separated by semicolons.  For instance, to enable platform abstraction *and* 
  # use Mono's old regular expression interpreter (which is slower, but has a
  # shorter setup time), uncomment the line below instead:
  # MonoSetEnv <%= this.MonoServerAlias %> MONO_IOMAP=all;MONO_OLD_RX=1

  MonoApplications <%= this.MonoServerAlias %> "/<%= this.ApplicationName %>:<%= this.DocumentRoot %>"
  <Location "/<%= this.ApplicationName %>">
    Allow from all
    Order allow,deny
    MonoSetServerAlias <%= this.MonoServerAlias %>
    SetHandler mono
  <% if (this.EnableModDeflate) 
{ %>  SetOutputFilter DEFLATE
    SetEnvIfNoCase Request_URI "\.(?:gif|jpe?g|png)$" no-gzip dont-vary
  <% } %></Location>
<% if (this.EnableModDeflate) { %><%="  "%><IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/javascript
  </IfModule>
<% } %>
<% if (this.IsVirtualHost) { %>
</VirtualHost><% 
   } %>