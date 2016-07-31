using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Microsoft.AspNet.SignalR;

namespace AqWeb
{
    public class SensorHub : Hub
    {
        public void Send(string name, string message)
        {
            // Call the broadcastMessage method to update clients.
            Clients.All.broadcastMessage(name, message);
        }

        public void Error(string message)
        {
            // TODO - Send an error event up as telemetry... App Insights likely.
            System.Diagnostics.Trace.TraceError(message);
        }

    }
}