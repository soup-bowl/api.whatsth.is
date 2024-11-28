namespace Whatsthis.API.Models
{
	public class WhoisData
	{
		public string? Domain { get; set; }
		public string? Registrar { get; set; }
		public string? Whois { get; set; }
		public List<string>? NameServers { get; set; }
		public DateTime? Created { get; set; }
		public DateTime? Updated { get; set; }
		public DateTime? Expires { get; set; }
	}
}
