<%@ Page Title="" Language="C#" MasterPageFile="FeaturePage.master" AutoEventWireup="true"
    CodeFile="Moma.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Scan for Mono Compatibility (MoMA)
</asp:Content>

<asp:Content ID="Content2" ContentPlaceHolderID="featurecontent" runat="Server">
    <div class="grid_10" style="width: 600px;">
        <h1>
            Scan for Mono Compatibility</h1>
        <br />
        <p>
            There are some common stumbling blocks that keep .NET applications from being able
            to run on Mono. These can be due to using parts of the .NET framework that Mono
            does not implement or implements differently, or reliance on native platform code
            like user32.
        </p>
        <br />
        <p>
            The <a href="http://www.mono-project.com/MoMA">Mono Migration Analyzer (MoMA)</a>
            can scan your compiled assemblies for these types of issues and point them out,
            making it easy to find them and work around them.
        </p>
        <br />
        <br />
        <h2>Step 1:</h2>
        <p>
            Open your solution in Visual Studio and ensure it compiles.
        </p>
        <br />
        <img class="shot" src="img/moma1.png" alt="Analyzing with MoMA - Step 1" />
        <br />
        <br />
        <h2>Step 2:</h2>
        <p>
            Select the Mono->Analyze for Mono Migration (MoMA) menu item.
        </p>
        <br />
        <img class="shot" src="img/moma2.png" alt="Analyzing with MoMA - Step 2" />
        <br />
        <br />
        <h2>Step 3:</h2>
        <p>
            MoMA will scan your application and look for code that may cause issues on Mono.
            These issues will be rated and placed in the Error List. Clicking them will take
            you to the affected code.
            </p>
        <br />
        <img class="shot" src="img/moma3.png" alt="Analyzing with MoMA - Step 3" />
        <br />
        <br />
        <br />
        <p>
            For details on the types of issues MoMA scans for, and how to fix them, please see
            the <a href="http://www.mono-project.com/MoMA_-_Issue_Descriptions">MoMA User's Guide</a>.
            </p>
        <br />
        <br />
    </div>
</asp:Content>
