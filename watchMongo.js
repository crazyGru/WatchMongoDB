const { MongoClient } = require('mongodb');

async function watchChanges() {
    const uri = 'mongodb+srv://admin:trustkmp123@cluster0.celqdib.mongodb.net'; // Replace with your MongoDB connection string
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        await client.connect();
        console.log('Connected to MongoDB');

        const database = client.db('harmony'); // Replace with your database name
        const collection = database.collection('profiles'); // Replace with your collection name

        // Create a change stream on the collection
        const changeStream = collection.watch();

        // Listen for changes
        changeStream.on('change', (change) => {
            switch (change.operationType) {
                case 'insert':
                    console.log('Document inserted:', change.fullDocument);
                    break;
                case 'update':
                    console.log('Document updated:', change.updateDescription);
                    break;
                case 'delete':
                    console.log('Document deleted:', change.documentKey);
                    break;
                default:
                    console.log('Other change:', change);
                    break;
            }
        });
        

    } catch (err) {
        console.error('Error connecting to MongoDB:', err);
    }
}

watchChanges().catch(console.error);
