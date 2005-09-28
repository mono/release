
using System;

namespace Novell.Utility
{
	class GuidGenerator
	{
		public static void Main(string []args )
		{
			string strGuid = System.Guid.NewGuid().ToString();
			Console.WriteLine(strGuid);
		}
	}
}


