using Whatsthis.API.Models;
using Whatsthis.API.Service;

namespace Whatsthis.API.Tests.Service
{
	public class InspectionServiceTests
	{
		private readonly IInspectionService _inspectService;

		public InspectionServiceTests()
		{
			InspectionEntity mockDetection = new InspectionEntity()
			{
				body = ["//html"],
				headers = ["content-type: text/html"],
				name = "Test",
				description = "Test Description",
				url = "https://www.example.com/test"
			};

			List<InspectionEntity> mockList = [mockDetection];

			_inspectService = new InspectionService("https://www.example.com", new InspectionSetup
			{
				cms = mockList,
				frontend = [],
				javascript = [],
				seo = [],
				cdn = [],
				language = [],
				server = []
			});
		}

		[Fact]
		public void Get_Should_Return_InspectionData()
		{
			InspectionData result = _inspectService.Get();

			Assert.NotNull(result);
			Assert.Equal("https://www.example.com", result.URL);
			Assert.Equal("Test", result.Technology.cms[0].Name);
			Assert.Equal(1, result.Technology.cms[0].MatchAvailable);
			Assert.Equal("//html", result.Technology.cms[0].MatchedOn[0]);
			Assert.NotNull(result.Technology);
		}
	}
}
