import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { config } from './config/index.js';
import { generateToken } from './token.js';

const currentModuleURL = import.meta.url;
const __filename = fileURLToPath(currentModuleURL);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get("/", (req, res) => {
  res.send(`Hello World!`);
});
app.use('/files', express.static(path.join(__dirname, 'data')));

app.get('/api/token?', generateToken);

app.listen(config.port, () => {
  console.log(`App listening on port ${config.port}!`);
});
