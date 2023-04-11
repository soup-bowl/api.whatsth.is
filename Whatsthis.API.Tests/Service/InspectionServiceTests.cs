using WhatsthisAPI.Models;
using WhatsthisAPI.Service;

namespace WhatsthisAPI.Tests
{
	public class InspectionServiceTests
	{
		private readonly IInspectionService _inspectService;

		public InspectionServiceTests()
		{
			InspectionEntity mockDetection = new InspectionEntity()
			{
				body = new List<string> { "//html" },
				headers = new List<string> { "content-type: text/html" },
				name = "Test",
				description = "Test Description",
				url = "https://www.example.com/test"
			};

			List<InspectionEntity> mockList = new List<InspectionEntity>();
			mockList.Add(mockDetection);

			_inspectService = new InspectionService("https://www.example.com", new InspectionSetup
			{
				cms = mockList,
				frontend = new List<InspectionEntity>(),
				javascript = new List<InspectionEntity>(),
				seo = new List<InspectionEntity>(),
				cdn = new List<InspectionEntity>(),
				language = new List<InspectionEntity>(),
				server = new List<InspectionEntity>()
			});
		}

		[Fact]
		public void Get_Should_Return_InspectionData()
		{
			InspectionData result = _inspectService.Get();

			//Console.WriteLine(JsonConvert.SerializeObject(result));

			Assert.NotNull(result);
			Assert.Equal("https://www.example.com", result.URL);
			Assert.Equal("Test", result.Technology.cms[0].Name);
			Assert.Equal(1, result.Technology.cms[0].MatchAvailable);
			Assert.Equal("//html", result.Technology.cms[0].MatchedOn[0]);
			Assert.NotNull(result.Technology);
		}
	}
}
