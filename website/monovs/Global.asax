<%@ Application Language="C#" %>

<script runat="server">

    void Application_Start(object sender, EventArgs e)
    {
        if (String.IsNullOrEmpty(ConfigurationManager.AppSettings["MonoVsDB"]))
            throw new ApplicationException("Missing connection string from configuration file.");
        if (String.IsNullOrEmpty(ConfigurationManager.AppSettings["MonoTools_msi"]))
            throw new ApplicationException("Missing msi installer filename (MonoTools_msi).");
        if (String.IsNullOrEmpty(ConfigurationManager.AppSettings["MonoTools_vsix"]))
            throw new ApplicationException("Missing vsix installer filename (MonoTools_vsix).");
    }
    
    void Application_End(object sender, EventArgs e) 
    {
        //  Code that runs on application shutdown

    }
        
    void Application_Error(object sender, EventArgs e) 
    { 
        // Code that runs when an unhandled error occurs

    }

    void Session_Start(object sender, EventArgs e) 
    {
        // Code that runs when a new session is started

    }

    void Session_End(object sender, EventArgs e) 
    {
        // Code that runs when a session ends. 
        // Note: The Session_End event is raised only when the sessionstate mode
        // is set to InProc in the Web.config file. If session mode is set to StateServer 
        // or SQLServer, the event is not raised.

    }
       
</script>
