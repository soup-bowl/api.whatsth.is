namespace WhatsthisAPI.Models
{
	public class InspectionResultInformation
	{
		public string? Name { get; set; }
		public string? Description { get; set; }
		public string? URL { get; set; }
		public int? MatchAvailable { get; set; }
		public List<string> MatchedOn { get; set; } = new List<string>();
	}
}
