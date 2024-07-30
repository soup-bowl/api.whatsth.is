using YamlDotNet.Serialization;
using WhatsthisAPI.Models;

namespace WhatsthisAPI.Service
{
	public interface IConfigurationService
	{
		InspectionSetup InspectionDefinitions { get; }
	}

	public class ConfigurationService : IConfigurationService
	{
		private readonly InspectionSetup _inspectionDefinitions;

		public ConfigurationService()
		{
			string defDefUrl = "https://gist.githubusercontent.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1/raw/definitions.yml";
			string defUrl = Environment.GetEnvironmentVariable("WTAPI_DEFINITION_URL") ?? defDefUrl;
			HttpClient httpClient = new HttpClient();

			using (Stream stream = httpClient.GetStreamAsync(defUrl).Result)
			using (StreamReader reader = new StreamReader(stream))
			{
				IDeserializer deserializer = new DeserializerBuilder().Build();
				_inspectionDefinitions = deserializer.Deserialize<InspectionSetup>(reader);
			}
		}

		public InspectionSetup InspectionDefinitions => _inspectionDefinitions;
	}
}
