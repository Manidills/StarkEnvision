import dotenv from 'dotenv';

dotenv.config();

export const config = {
    port: process.env.PORT || 5000,
    voyager: {
        apiKey: process.env.VOYAGER_API_KEY,
    }
};
