using Whatsthis.API.Models;
using Whatsthis.API.Service;

namespace Whatsthis.API.Tests.Service
{
	public class DnsServiceTests
	{
		private readonly IDnsService _dnsService;

		public DnsServiceTests()
		{
			_dnsService = new DnsService();
		}

		[Fact]
		public void Get_Returns_DnsData_With_Results()
		{
			string url = "example.com";

			DnsData dnsData = _dnsService.Get(url);

			Assert.NotNull(dnsData);
			Assert.NotEmpty(dnsData.A);
			Assert.NotEmpty(dnsData.AAAA);
			Assert.NotEmpty(dnsData.MX);
			Assert.NotEmpty(dnsData.NS);
			Assert.NotEmpty(dnsData.TXT);

			DnsMailData firstMxResult = dnsData.MX[0];
			Assert.Equal("example.com.", firstMxResult.Address);
			Assert.Equal(0, firstMxResult.Priority);
		}

		[Fact]
		public void Get_Returns_DnsData_With_No_Results()
		{
			string url = "thisdomaindoesnotexist1234567890.com";

			DnsData dnsData = _dnsService.Get(url);

			Assert.NotNull(dnsData);
			Assert.Empty(dnsData.A);
			Assert.Empty(dnsData.AAAA);
			Assert.Empty(dnsData.CNAME);
			Assert.Empty(dnsData.MX);
			Assert.Empty(dnsData.NS);
			Assert.Empty(dnsData.TXT);
		}
	}
}
