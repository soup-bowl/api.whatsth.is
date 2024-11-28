using Whatsthis.API.Models;
using Whatsthis.API.Service;

namespace Whatsthis.API.Tests.Service
{
	public class ConfigurationServiceTests
	{
		private readonly ConfigurationService _configService;

		public ConfigurationServiceTests()
		{
			_configService = new ConfigurationService();
		}

		[Fact]
		public void TestInspectionDefinitions()
		{
			InspectionSetup inspectionDefinitions = _configService.InspectionDefinitions;

			Assert.NotNull(inspectionDefinitions);
			Assert.NotEmpty(inspectionDefinitions.cms);
			Assert.NotEmpty(inspectionDefinitions.frontend);
			Assert.NotEmpty(inspectionDefinitions.javascript);
			Assert.NotEmpty(inspectionDefinitions.seo);
			Assert.NotEmpty(inspectionDefinitions.cdn);
			Assert.NotEmpty(inspectionDefinitions.language);
			Assert.NotEmpty(inspectionDefinitions.server);
		}
	}
}
