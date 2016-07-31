using Microsoft.AspNet.SignalR.Client;
using Microsoft.ServiceBus.Messaging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AqBroker
{
    class SimpleEventProcessor : IEventProcessor
    {
        Stopwatch checkpointStopWatch;
        HubConnection hubConnection;
        IHubProxy sensorHubProxy;

        async Task IEventProcessor.CloseAsync(PartitionContext context, CloseReason reason)
        {
            Trace.TraceInformation("Processor Shutting Down. Partition '{0}', Reason: '{1}'.", context.Lease.PartitionId, reason);
            if (reason == CloseReason.Shutdown)
            {
                await context.CheckpointAsync();
            }
        }

        async Task IEventProcessor.OpenAsync(PartitionContext context)
        {
            Trace.TraceInformation("SimpleEventProcessor initialized.  Partition: '{0}', Offset: '{1}'", context.Lease.PartitionId, context.Lease.Offset);

        
            this.checkpointStopWatch = new Stopwatch();
            this.checkpointStopWatch.Start();


            hubConnection = new HubConnection("http://localhost:14829/");
            sensorHubProxy = hubConnection.CreateHubProxy("SensorHub");
            await hubConnection.Start();
            Trace.TraceInformation("Signlar R Client (Worker) started.");

            await Task.FromResult<object>(null);
        }

        async Task IEventProcessor.ProcessEventsAsync(PartitionContext context, IEnumerable<EventData> messages)
        {
            foreach (EventData eventData in messages)
            {
                string data = Encoding.UTF8.GetString(eventData.GetBytes());

                JToken token = JObject.Parse(data);
                string type = (string)token.SelectToken("type");

                try
                {
                    if (type.Equals("Reading"))
                    {
                        await sensorHubProxy.Invoke("Send", "Reading (" + context.Lease.PartitionId + ")", data);
                    }
                    else if (type.Equals("Alert"))
                    {
                        await sensorHubProxy.Invoke("Send", "Alert (" + context.Lease.PartitionId + ")", data);
                    }
                    else
                    {
                        await sensorHubProxy.Invoke("Error", "Error (" + context.Lease.PartitionId + ")", data);
                    }
                }
                catch(NullReferenceException e)
                {
                    await sensorHubProxy.Invoke("Error", "Error (" + context.Lease.PartitionId + ")", data);
                    Trace.TraceInformation(string.Format("Could not parse message type.  Partition: '{0}', Data: '{1}'",
                    context.Lease.PartitionId, data));
                    continue;
                }
                Trace.TraceInformation(string.Format("Message received.  Partition: '{0}', Data: '{1}'",
                    context.Lease.PartitionId, data));

            }

            //Call checkpoint every 5 minutes, so that worker can resume processing from 5 minutes back if it restarts.
            if (this.checkpointStopWatch.Elapsed > TimeSpan.FromSeconds(10))
            {
                await context.CheckpointAsync();
                this.checkpointStopWatch.Restart();
            }
        }
    }
}
