namespace Whatsthis.API.Models
{
	public class DnsData
	{
		public List<string> A { get; set; } = new List<string>();
		public List<string> AAAA { get; set; } = new List<string>();
		public List<string> CNAME { get; set; } = new List<string>();
		public List<DnsMailData> MX { get; set; } = new List<DnsMailData>();
		public List<string> TXT { get; set; } = new List<string>(); 
		public List<string> NS { get; set; } = new List<string>();
	}
}
