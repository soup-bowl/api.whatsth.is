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
			string defDefUrl = "https://gist.githubusercontent.com/soup-bowl/ac51dd12d69814a366d56c7a7eb6a3ad/raw/e2d9ac00b161aa530d2dbcff8ac90ecf33971769/gistfile1.yaml";
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
