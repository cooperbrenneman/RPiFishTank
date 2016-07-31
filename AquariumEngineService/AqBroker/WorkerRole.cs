using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.Diagnostics;
using Microsoft.WindowsAzure.ServiceRuntime;
using Microsoft.WindowsAzure.Storage;
using Microsoft.AspNet.SignalR.Client;
using Microsoft.ServiceBus.Messaging;

namespace AqBroker
{
    public class WorkerRole : RoleEntryPoint
    {
        private readonly CancellationTokenSource cancellationTokenSource = new CancellationTokenSource();
        private readonly ManualResetEvent runCompleteEvent = new ManualResetEvent(false);

        public override void Run()
        {
            Trace.TraceInformation("AqBroker is running");

            try
            {
                this.RunAsync(this.cancellationTokenSource.Token).Wait();
            }
            finally
            {
                this.runCompleteEvent.Set();
            }
        }

        public override bool OnStart()
        {
            // Set the maximum number of concurrent connections
            ServicePointManager.DefaultConnectionLimit = 12;

            // For information on handling configuration changes
            // see the MSDN topic at http://go.microsoft.com/fwlink/?LinkId=166357.

            bool result = base.OnStart();

            Trace.TraceInformation("AqBroker has been started");

            return result;
        }

        public override void OnStop()
        {
            Trace.TraceInformation("AqBroker is stopping");

            this.cancellationTokenSource.Cancel();
            this.runCompleteEvent.WaitOne();

            base.OnStop();

            Trace.TraceInformation("AqBroker has stopped");
        }

        private async Task RunAsync(CancellationToken cancellationToken)
        {
            // TODO: Replace the following with your own logic.

            string eventHubConnectionString = "Endpoint=sb://aqengine.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=lEXD5lO2WvuazbbZDluqttBAT5mCsl+9GIgGjBW/WQM=";
            string eventHubName = "aqengine";
            string storageAccountName = "aqengine";
            string storageAccountKey = "FaNYy2bM6/Z2m99pGSqvkq/bIG4ot9CN28Y+Hlq5oiUvhPla/Y2EqkM4AbdnrKpFPu6/twC5rU7oUfGJRWugNg==";
            string storageConnectionString = string.Format("DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1}", storageAccountName, storageAccountKey);

            string eventProcessorHostName = Guid.NewGuid().ToString();
            EventProcessorHost eventProcessorHost = new EventProcessorHost(eventProcessorHostName, eventHubName, EventHubConsumerGroup.DefaultGroupName, eventHubConnectionString, storageConnectionString);
            Trace.TraceInformation("Registering EventProcessor...");
            var options = new EventProcessorOptions();
            options.ExceptionReceived += (sender, e) => { Console.WriteLine(e.Exception); };
            eventProcessorHost.RegisterEventProcessorAsync<SimpleEventProcessor>(options).Wait();


            /*var hubConnection = new HubConnection("http://localhost:14829/");
            IHubProxy sensorHubProxy = hubConnection.CreateHubProxy("SensorHub");
            await hubConnection.Start();
            Trace.TraceInformation("Signlar R Client (Worker) started.");*/

            while (!cancellationToken.IsCancellationRequested)
            {
                //await sensorHubProxy.Invoke("Send", "Kelly", "Testing this out");
                await Task.Delay(1000);
            }
        }
    }
}
