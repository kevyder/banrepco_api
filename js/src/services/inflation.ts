export async function fetchLatestInflation(url: string) {
  const options = {
    method: 'GET',
    headers: {
      accept: 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      connection: 'keep-alive',
      'content-type': 'application/json; charset=utf-8',
      cookie: '_gid=GA1.3.1301051833.1767122223; X-Oracle-BMC-LBS-Route=f9ac770283cc12a4c51c6fe6cea79b887f20a86b; uzmx=7f90009cd2dda6-bd71-437d-9f83-779c9320323c19-173549439698531635172578-5da2b37cf3e84f07157; uzmxj=7f90009cd2dda6-bd71-437d-9f83-779c9320323c9-17586422069408487363353-8b2def96ca502bab73; _gat_UA-2791658-1=1; _ga_XKKJ6KGNH7=GS2.1.s1767128608$o2$g1$t1767129575$j60$l0$h0; _ga=GA1.3.1475254602.1767122223; _ga_MKP83SEF5M=GS2.3.s1767128609$o2$g1$t1767129581$j54$l0$h0',
      referer: 'https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/100001/inflacion_y_meta',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'sec-gpc': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }
  };

  try {
    const response = await fetch(url, options);
    const data = await response.json();
    const lastMonthTarget = data["SERIES"][0]["data"].pop();
    const lastMonthInflation = data["SERIES"][1]["data"].pop()

    const target = lastMonthTarget[1]
    const inflation = lastMonthInflation[1]

    const inflationDateTimestamp = lastMonthInflation[0];
    const inflationDate = new Date(inflationDateTimestamp);
    const year = inflationDate.getUTCFullYear();
    const month = inflationDate.getUTCMonth() + 1; // Months are zero-based

    return { year, month, inflation, target };
  } catch (error) {
    console.error(error);
  }
}
