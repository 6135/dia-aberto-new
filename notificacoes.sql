--
-- Create model EmissorMensagem
--
CREATE TABLE `EmissorMensagem` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY);
--
-- Create model RecetorMensagem
--
CREATE TABLE `RecetorMensagem` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `mensagem_id` integer NOT NULL);
ALTER TABLE `RecetorMensagem` ADD CONSTRAINT `RecetorMensagem_mensagem_id_83e187cf_fk_Notificacao_id` FOREIGN KEY (`mensagem_id`) REFERENCES `Notificacao` (`id`);
--
-- Add field recetor to recetormensagem
--
ALTER TABLE `RecetorMensagem` ADD COLUMN `recetor_id` integer NOT NULL , ADD CONSTRAINT `RecetorMensagem_recetor_id_a3da4150_fk_Utilizador_user_ptr_id` FOREIGN KEY (`recetor_id`) REFERENCES `Utilizador`(`user_ptr_id`);
--
-- Add field emissor to emissormensagem
--
ALTER TABLE `EmissorMensagem` ADD COLUMN `emissor_id` integer NOT NULL , ADD CONSTRAINT `EmissorMensagem_emissor_id_fbb1310d_fk_Utilizador_user_ptr_id` FOREIGN KEY (`emissor_id`) REFERENCES `Utilizador`(`user_ptr_id`);
--
-- Add field mensagem to emissormensagem
--
ALTER TABLE `EmissorMensagem` ADD COLUMN `mensagem_id` integer NOT NULL , ADD CONSTRAINT `EmissorMensagem_mensagem_id_d1314a9b_fk_Notificacao_id` FOREIGN KEY (`mensagem_id`) REFERENCES `Notificacao`(`id`);
