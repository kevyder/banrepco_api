import { XMLParser } from 'fast-xml-parser';

interface TRMResponse {
  'message:GenericData': {
    'message:DataSet': {
      'generic:Series': {
        'generic:Obs': {
          'generic:ObsValue': {
            '@_value': string;
          };
        };
      };
    };
  };
}

export async function fetchLatestTRM(url: string): Promise<number> {
  try {
    const myHeaders = new Headers();
    myHeaders.append("Accept", "*/*");

    const requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow" as const
    };

    const response = await fetch(
      `${url}/ESTAT,DF_TRM_DAILY_LATEST,1.0/`,
      requestOptions
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const xmlText = await response.text();
    const parser = new XMLParser({
      ignoreAttributes: false,
      attributeNamePrefix: '@_'
    });

    const result = parser.parse(xmlText) as TRMResponse;
    const trmValue = parseFloat(
      result['message:GenericData']['message:DataSet']['generic:Series']['generic:Obs']['generic:ObsValue']['@_value']
    );

    if (isNaN(trmValue)) {
      throw new Error('Invalid TRM value received');
    }

    return trmValue;
  } catch (error) {
    console.error('Error fetching TRM:', error);
    throw error;
  }
}
