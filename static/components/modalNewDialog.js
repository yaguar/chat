import React from 'react';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import SearchField from "react-search-field";

const ModalNewDialog = (props) => {
    const handleClose = () => props.visible(false)
    return (
        <Modal show={props.show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Создать чат</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <SearchField
                          placeholder="Search..."
                        />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary">
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    );
}

export default ModalNewDialog;