describe('Test APIs with login', () => {

  beforeEach(() => {
    
    // --------------------------
    // API para realizar el login
    // --------------------------
    cy.request({
      method: 'POST',
      url: 'http://localhost:5001/api/auth/login',
      headers:{
              'Content-Type':'application/json'
              },
      body:{
        username:"nicolasbarone@gmail.com",
        password: "123"
      }        
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body.msg).to.equal("login succesful")
    })

  });


  // ----------------------------------------------------
  // API para obtener todas las disciplinas de un miembro
  // ---------------------------------------------------- 
  it('API Me test Disciplines by Member', () => {  
    cy.request({
        method: 'GET',
        url: 'http://localhost:5001/api/me/disciplines',
        headers:{
                'Content-Type':'application/json',
                'Authorization': 1
                }
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body[0].active).to.equal(true)
      expect(response.body[0].category).to.equal('Armas')
    })
  })



  // ----------------------------------------
  // API para obtener el Perfil de un miembro
  // ----------------------------------------
  it('API Me test Profile of some member', () => {
    cy.request({
      method: 'GET',
      url: 'http://localhost:5001/api/me/profile',
      headers:{
              'Content-Type':'application/json',
              'Authorization': 1
              }
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body.first_name).to.equal('Nicolas')
      expect(response.body.last_name).to.equal('Barone')
    })
  })


  // ----------------------------------------
  // API para obtener los pagos de un miembro
  // ----------------------------------------
  it('API Me test Payments of some member', () => {
    cy.request({
      method: 'GET',
      url: 'http://localhost:5001/api/me/payments',
      headers:{
              'Content-Type':'application/json',
              'Authorization': 1
              }
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body[0].paid).to.equal(true)
      expect(response.body[0].month).to.equal(6)
      expect(response.body[0].amount).to.equal(1760.0)
    })
  })


  // ----------------------------------------
  // API para obtener las licencias de un miembro
  // ----------------------------------------
  it('API Me test License of some member', () => {
    cy.request({
      method: 'GET',
      url: 'http://localhost:5001/api/me/license',
      headers:{
              'Content-Type':'application/json',
              'Authorization': 1
              }
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body.description).to.equal('El miembro no presenta ninguna deuda')
    })
  })
})