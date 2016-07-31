<?xml version="1.0" encoding="utf-8"?>
<serviceModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" name="AqEngineService2" generation="1" functional="0" release="0" Id="4102f820-79c2-4f74-a444-a597b3f7018d" dslVersion="1.2.0.0" xmlns="http://schemas.microsoft.com/dsltools/RDSM">
  <groups>
    <group name="AqEngineService2Group" generation="1" functional="0" release="0">
      <componentports>
        <inPort name="AqWeb:Endpoint1" protocol="http">
          <inToChannel>
            <lBChannelMoniker name="/AqEngineService2/AqEngineService2Group/LB:AqWeb:Endpoint1" />
          </inToChannel>
        </inPort>
      </componentports>
      <settings>
        <aCS name="AqBroker:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" defaultValue="">
          <maps>
            <mapMoniker name="/AqEngineService2/AqEngineService2Group/MapAqBroker:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" />
          </maps>
        </aCS>
        <aCS name="AqBrokerInstances" defaultValue="[1,1,1]">
          <maps>
            <mapMoniker name="/AqEngineService2/AqEngineService2Group/MapAqBrokerInstances" />
          </maps>
        </aCS>
        <aCS name="AqWeb:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" defaultValue="">
          <maps>
            <mapMoniker name="/AqEngineService2/AqEngineService2Group/MapAqWeb:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" />
          </maps>
        </aCS>
        <aCS name="AqWebInstances" defaultValue="[1,1,1]">
          <maps>
            <mapMoniker name="/AqEngineService2/AqEngineService2Group/MapAqWebInstances" />
          </maps>
        </aCS>
      </settings>
      <channels>
        <lBChannel name="LB:AqWeb:Endpoint1">
          <toPorts>
            <inPortMoniker name="/AqEngineService2/AqEngineService2Group/AqWeb/Endpoint1" />
          </toPorts>
        </lBChannel>
      </channels>
      <maps>
        <map name="MapAqBroker:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" kind="Identity">
          <setting>
            <aCSMoniker name="/AqEngineService2/AqEngineService2Group/AqBroker/Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" />
          </setting>
        </map>
        <map name="MapAqBrokerInstances" kind="Identity">
          <setting>
            <sCSPolicyIDMoniker name="/AqEngineService2/AqEngineService2Group/AqBrokerInstances" />
          </setting>
        </map>
        <map name="MapAqWeb:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" kind="Identity">
          <setting>
            <aCSMoniker name="/AqEngineService2/AqEngineService2Group/AqWeb/Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" />
          </setting>
        </map>
        <map name="MapAqWebInstances" kind="Identity">
          <setting>
            <sCSPolicyIDMoniker name="/AqEngineService2/AqEngineService2Group/AqWebInstances" />
          </setting>
        </map>
      </maps>
      <components>
        <groupHascomponents>
          <role name="AqBroker" generation="1" functional="0" release="0" software="C:\Users\ksmit\Source\AqEngineService2\AqEngineService2\csx\Debug\roles\AqBroker" entryPoint="base\x64\WaHostBootstrapper.exe" parameters="base\x64\WaWorkerHost.exe " memIndex="-1" hostingEnvironment="consoleroleadmin" hostingEnvironmentVersion="2">
            <settings>
              <aCS name="Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" defaultValue="" />
              <aCS name="__ModelData" defaultValue="&lt;m role=&quot;AqBroker&quot; xmlns=&quot;urn:azure:m:v1&quot;&gt;&lt;r name=&quot;AqBroker&quot; /&gt;&lt;r name=&quot;AqWeb&quot;&gt;&lt;e name=&quot;Endpoint1&quot; /&gt;&lt;/r&gt;&lt;/m&gt;" />
            </settings>
            <resourcereferences>
              <resourceReference name="DiagnosticStore" defaultAmount="[4096,4096,4096]" defaultSticky="true" kind="Directory" />
              <resourceReference name="EventStore" defaultAmount="[1000,1000,1000]" defaultSticky="false" kind="LogStore" />
            </resourcereferences>
          </role>
          <sCSPolicy>
            <sCSPolicyIDMoniker name="/AqEngineService2/AqEngineService2Group/AqBrokerInstances" />
            <sCSPolicyUpdateDomainMoniker name="/AqEngineService2/AqEngineService2Group/AqBrokerUpgradeDomains" />
            <sCSPolicyFaultDomainMoniker name="/AqEngineService2/AqEngineService2Group/AqBrokerFaultDomains" />
          </sCSPolicy>
        </groupHascomponents>
        <groupHascomponents>
          <role name="AqWeb" generation="1" functional="0" release="0" software="C:\Users\ksmit\Source\AqEngineService2\AqEngineService2\csx\Debug\roles\AqWeb" entryPoint="base\x64\WaHostBootstrapper.exe" parameters="base\x64\WaIISHost.exe " memIndex="-1" hostingEnvironment="frontendadmin" hostingEnvironmentVersion="2">
            <componentports>
              <inPort name="Endpoint1" protocol="http" portRanges="80" />
            </componentports>
            <settings>
              <aCS name="Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" defaultValue="" />
              <aCS name="__ModelData" defaultValue="&lt;m role=&quot;AqWeb&quot; xmlns=&quot;urn:azure:m:v1&quot;&gt;&lt;r name=&quot;AqBroker&quot; /&gt;&lt;r name=&quot;AqWeb&quot;&gt;&lt;e name=&quot;Endpoint1&quot; /&gt;&lt;/r&gt;&lt;/m&gt;" />
            </settings>
            <resourcereferences>
              <resourceReference name="DiagnosticStore" defaultAmount="[4096,4096,4096]" defaultSticky="true" kind="Directory" />
              <resourceReference name="EventStore" defaultAmount="[1000,1000,1000]" defaultSticky="false" kind="LogStore" />
            </resourcereferences>
          </role>
          <sCSPolicy>
            <sCSPolicyIDMoniker name="/AqEngineService2/AqEngineService2Group/AqWebInstances" />
            <sCSPolicyUpdateDomainMoniker name="/AqEngineService2/AqEngineService2Group/AqWebUpgradeDomains" />
            <sCSPolicyFaultDomainMoniker name="/AqEngineService2/AqEngineService2Group/AqWebFaultDomains" />
          </sCSPolicy>
        </groupHascomponents>
      </components>
      <sCSPolicy>
        <sCSPolicyUpdateDomain name="AqWebUpgradeDomains" defaultPolicy="[5,5,5]" />
        <sCSPolicyUpdateDomain name="AqBrokerUpgradeDomains" defaultPolicy="[5,5,5]" />
        <sCSPolicyFaultDomain name="AqBrokerFaultDomains" defaultPolicy="[2,2,2]" />
        <sCSPolicyFaultDomain name="AqWebFaultDomains" defaultPolicy="[2,2,2]" />
        <sCSPolicyID name="AqBrokerInstances" defaultPolicy="[1,1,1]" />
        <sCSPolicyID name="AqWebInstances" defaultPolicy="[1,1,1]" />
      </sCSPolicy>
    </group>
  </groups>
  <implements>
    <implementation Id="08642f0e-b513-4311-bec4-1e7f3ecb3532" ref="Microsoft.RedDog.Contract\ServiceContract\AqEngineService2Contract@ServiceDefinition">
      <interfacereferences>
        <interfaceReference Id="d199fec6-8205-4178-b33b-2acef116b4cd" ref="Microsoft.RedDog.Contract\Interface\AqWeb:Endpoint1@ServiceDefinition">
          <inPort>
            <inPortMoniker name="/AqEngineService2/AqEngineService2Group/AqWeb:Endpoint1" />
          </inPort>
        </interfaceReference>
      </interfacereferences>
    </implementation>
  </implements>
</serviceModel>