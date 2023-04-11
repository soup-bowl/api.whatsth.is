using WhatsthisAPI.Models;
using WhatsthisAPI.Service;

namespace WhatsthisAPI.Tests
{
	public class WhoisServiceTests
	{
		private readonly IWhoisService _doctorWho;

		public WhoisServiceTests()
		{
			_doctorWho = new WhoisService();
		}

		[Fact]
		public void Get_ReturnsWhoisData()
		{
			string url = "google.com";

			WhoisData result = _doctorWho.Get(url);

			Assert.IsType<WhoisData>(result);
			Assert.Equal("google.com", result.Domain);
		}
	}
}
