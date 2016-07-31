using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AqBroker
{
    class SensorSchema
    {
        [JsonConverter(typeof(StringEnumConverter))]
        enum type { Reading, Alert, Error }
        string message { get; set; }
    }


    class SensorData : SensorSchema
    {
        string sensor;
        string sensorName;
        DateTime timestamp;
        double value;
    }

    class SensorError : SensorSchema
    {
        int errorCode;
    }

    class SensorAlert : SensorData
    {
        double threshold;

        [JsonConverter(typeof(StringEnumConverter))]
        enum op { LessThan, GreaterThan, NotEqual, Equal }
    }
}
