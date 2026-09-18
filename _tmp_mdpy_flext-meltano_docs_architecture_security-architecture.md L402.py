# from flext-meltano/docs/architecture/security-architecture.md:402
from __future__ import annotations


class DataEncryptor:
    """Enterprise-grade data encryption service."""

    def __init__(self, kms_client, algorithm: str = "AES-256-GCM"):
        self.kms = kms_client
        self.algorithm = algorithm

    def encrypt_data(self, plaintext: bytes, context: Dict[str, str]) -> EncryptedData:
        """Encrypt data with envelope encryption."""
        # Generate data key
        data_key = self.kms.generate_data_key(
            key_spec="AES_256", encryption_context=context
        )

        # Encrypt data with data key
        encrypted_data = self._encrypt_with_data_key(plaintext, data_key.plaintext)

        # Encrypt data key with master key
        encrypted_key = self.kms.encrypt(
            key_id=self.master_key_id,
            plaintext=data_key.plaintext,
            encryption_context=context,
        )

        return EncryptedData(
            encrypted_data=encrypted_data,
            encrypted_key=encrypted_key.ciphertext_blob,
            key_id=self.master_key_id,
            algorithm=self.algorithm,
            context=context,
        )

    def decrypt_data(self, encrypted_data: EncryptedData) -> bytes:
        """Decrypt data with envelope decryption."""
        # Decrypt data key
        decrypted_key = self.kms.decrypt(
            key_id=encrypted_data.key_id,
            ciphertext_blob=encrypted_data.encrypted_key,
            encryption_context=encrypted_data.context,
        )

        # Decrypt data with data key
        return self._decrypt_with_data_key(
            encrypted_data.encrypted_data, decrypted_key.plaintext
        )```
#### In-Transit Encryption

