namespace WhatsthisAPI.Models
{
	public class InspectionEntity
	{
		public string? name { get; set; }
		public string? description { get; set; }
		public string? url { get; set; }
		public List<string> headers { get; set; } = new List<string>();
		public List<string> body { get; set; } = new List<string>();
	}
}
