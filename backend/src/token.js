import axios from "axios";
import path from 'path';
import { fileURLToPath } from 'url';
import { createObjectCsvWriter as createCsvWriter } from 'csv-writer';
import { config } from './config/index.js';

const currentModuleURL = import.meta.url;
const __filename = fileURLToPath(currentModuleURL);
const __dirname = path.dirname(__filename);

async function fetchTokensErc20() {
  const allItems = [];
  let lastPage = 1;

  // Fetch the first page to get the lastPage value
  try {
    const initialResponse = await axios({
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: "erc20",
        ps: 100,
        p: 1,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    });

    // Get lastPage from the initial response
    lastPage = initialResponse.data.lastPage;
    console.log(`Total pages to fetch: ${lastPage}`);

    // Collect items from the first page
    allItems.push(...initialResponse.data.items);
  } catch (error) {
    console.error("Error fetching the first page:", error);
    return; // Exit if the first page fails
  }

  // Fetch remaining pages
  for (let p = 2; p <= lastPage; p++) {
    const options = {
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: "erc20",
        ps: 100,
        p: p,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    };

    try {
      const response = await axios(options);
      const items = response.data.items;
      allItems.push(...items); // Collect items from each page
    } catch (error) {
      console.error(`Error fetching page ${p}:`, error);
    }
  }

  // Define the CSV writer
  const csvWriter = createCsvWriter({
    path: "tokens_erc20.csv",
    header: [
      { id: "address", title: "Address" },
      { id: "decimals", title: "Decimals" },
      { id: "holders", title: "Holders" },
      { id: "name", title: "Name" },
      { id: "symbol", title: "Symbol" },
      { id: "transfers", title: "Transfers" },
      { id: "type", title: "Type" },
    ],
  });

  // Write all items to CSV
  try {
    await csvWriter.writeRecords(allItems);
    console.log("CSV file created successfully");
  } catch (error) {
    console.error("Error writing to CSV:", error);
  }
}

async function fetchTokensErc721() {
  const allItems = [];
  let lastPage = 1;

  // Fetch the first page to get the lastPage value
  try {
    const initialResponse = await axios({
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: "erc721",
        ps: 100,
        p: 1,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    });

    // Get lastPage from the initial response
    lastPage = initialResponse.data.lastPage;
    console.log(`Total pages to fetch: ${lastPage}`);

    // Collect items from the first page
    allItems.push(...initialResponse.data.items);
  } catch (error) {
    console.error("Error fetching the first page:", error);
    return; // Exit if the first page fails
  }

  // Fetch remaining pages
  for (let p = 2; p <= lastPage; p++) {
    const options = {
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: "erc721",
        ps: 100,
        p: p,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    };

    try {
      const response = await axios(options);
      const items = response.data.items;
      allItems.push(...items); // Collect items from each page
    } catch (error) {
      console.error(`Error fetching page ${p}:`, error);
    }
  }

  // Define the CSV writer
  const csvWriter = createCsvWriter({
    path: "tokens_erc721.csv",
    header: [
      { id: "address", title: "Address" },
      { id: "decimals", title: "Decimals" },
      { id: "holders", title: "Holders" },
      { id: "name", title: "Name" },
      { id: "symbol", title: "Symbol" },
      { id: "transfers", title: "Transfers" },
      { id: "type", title: "Type" },
    ],
  });

  // Write all items to CSV
  try {
    await csvWriter.writeRecords(allItems);
    console.log("CSV file created successfully");
  } catch (error) {
    console.error("Error writing to CSV:", error);
  }
}

async function fetchTokensErc1155() {
  const allItems = [];
  let lastPage = 1;

  // Fetch the first page to get the lastPage value
  try {
    const initialResponse = await axios({
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: "erc1155",
        ps: 100,
        p: 1,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    });

    // Get lastPage from the initial response
    lastPage = initialResponse.data.lastPage;
    console.log(`Total pages to fetch: ${lastPage}`);

    // Collect items from the first page
    allItems.push(...initialResponse.data.items);
  } catch (error) {
    console.error("Error fetching the first page:", error);
    return; // Exit if the first page fails
  }

  // Fetch remaining pages
  for (let p = 2; p <= lastPage; p++) {
    const options = {
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: "erc1155",
        ps: 100,
        p: p,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    };

    try {
      const response = await axios(options);
      const items = response.data.items;
      allItems.push(...items); // Collect items from each page
    } catch (error) {
      console.error(`Error fetching page ${p}:`, error);
    }
  }

  // Define the CSV writer
  const csvWriter = createCsvWriter({
    path: "tokens_erc1155.csv",
    header: [
      { id: "address", title: "Address" },
      { id: "decimals", title: "Decimals" },
      { id: "holders", title: "Holders" },
      { id: "name", title: "Name" },
      { id: "symbol", title: "Symbol" },
      { id: "transfers", title: "Transfers" },
      { id: "type", title: "Type" },
    ],
  });

  // Write all items to CSV
  try {
    await csvWriter.writeRecords(allItems);
    console.log("CSV file created successfully");
  } catch (error) {
    console.error("Error writing to CSV:", error);
  }
}
// Call the async function
// fetchTokensErc20();
// fetchTokensErc721();
// fetchTokensErc1155();

export const generateToken = async (req, res) => {
  const { tokenType } = req.query;
  if (!["erc20", "erc721", "erc1155" ].includes(tokenType)) {
  return res.status(400).json({ message: 'invalid token type', tokenTypes: ["erc20", "erc721", "erc1155"]});
  }
  const allItems = [];
  let lastPage = 1;

  // Fetch the first page to get the lastPage value
  try {
    const initialResponse = await axios({
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: tokenType,
        ps: 100,
        p: 1,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    });

    // Get lastPage from the initial response
    lastPage = initialResponse.data.lastPage;
    console.log(`Total pages to fetch: ${lastPage}`);

    // Collect items from the first page
    allItems.push(...initialResponse.data.items);
  } catch (error) {
    console.error("Error fetching the first page:", error);
    return; // Exit if the first page fails
  }

  // Fetch remaining pages
  for (let p = 2; p <= lastPage; p++) {
    const options = {
      method: "GET",
      url: "https://api.voyager.online/beta/tokens",
      params: {
        attribute: "holders",
        type: tokenType,
        ps: 100,
        p: p,
      },
      headers: {
        accept: "application/json",
        "x-api-key": config.voyager.apiKey,
      },
    };

    try {
      const response = await axios(options);
      const items = response.data.items;
      allItems.push(...items); // Collect items from each page
    } catch (error) {
      console.error(`Error fetching page ${p}:`, error);
    }
  }

  const filePath = path.join(__dirname, `../src/data/tokens_${tokenType}.csv`);
  // Define the CSV writer
  const csvWriter = createCsvWriter({
    path: filePath,
    header: [
      { id: "address", title: "Address" },
      { id: "decimals", title: "Decimals" },
      { id: "holders", title: "Holders" },
      { id: "name", title: "Name" },
      { id: "symbol", title: "Symbol" },
      { id: "transfers", title: "Transfers" },
      { id: "type", title: "Type" },
    ],
  });

  // Write all items to CSV
  try {
    await csvWriter.writeRecords(allItems);
    console.log("CSV file created successfully");
    res.status(200).json({ message: "CSV file created successfully", filePath: `https://starkhack.onrender.com/files/tokens_${tokenType}.csv` });
  } catch (error) {
    console.error("Error writing to CSV:", error);
    res.status(400).json({ message: "CSV file creation failed" });
  }
};
